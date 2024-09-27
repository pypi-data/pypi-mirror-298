from sklearn.feature_extraction.text import TfidfTransformer 
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import normalize
from sklearn.utils.extmath import safe_sparse_dot
from sklearn.utils.extmath import randomized_svd

from scipy.sparse.linalg import svds
from scipy.sparse import coo_matrix
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import inv
from scipy.spatial import cKDTree

from numpy.core.umath_tests import inner1d
from numpy.linalg import matrix_rank
import numexpr as ne
import numpy as np
import hdbscan
from umap.umap_ import UMAP
import time


class TriTan():
    def __init__(self,
                n_modalities = 2,
                res_size = 10,
                feature_granularity = 100,               
                epoch_phase_1 = 20,               
                epoch_phase_2 = 30,               
                resolution = 0.6,
                complexity = 5,
                precomputed = False,
                svd_mods = None, #用户自己提前算好的[u,v]字典
                n_component= {'RNA': [20,50], 'ATAC': [20,50]}): #每个模态的svd分解的维度 无论是不是提前算好 都要输入
        
        #read
        self.n_modalities = n_modalities
        self.feature_granularity = feature_granularity
        self.epoch_phase_1 = epoch_phase_1
        self.epoch_phase_2 = epoch_phase_2
        self.complexity = complexity        
        self.resolution = res_size
        self.res = int(resolution*100)
        self.n_component = n_component
        #check
        self.precomputed = precomputed
        self.svd_mods = svd_mods

        
        if self.n_modalities > 2:
            if self.svd_mods is not None:
                if len(self.svd_mods) <= 2:
                    raise ValueError('The number of svd components should match to the number of modalities')
            if len(self.n_component) <= 2 :
                raise ValueError('The number of svd components should match to the number of modalities')
        
        
        self.loss=[]
        #self.loss_atac =[]
        #self.loss_rna = []
        self.epoch_times =[]
        
        
    
    def fit(self, mdata):
        self.mods = list(mdata.mod)
        
        X_mods = {}
        self.n_features = {}  

        for mod in self.mods:
            X_mod, m , n = self.load(mdata, mod)
            X_mods[mod] = X_mod
            self.n_features[mod] = n

        
        self.n_cells = m

        S_mods, G_mods, ww_mods = self.initialize_(X_mods)
        
        iteration=0                
        u_mods ={}
        v_mods = {}
        C_mods = {}
        D_mods = {}
        

        if self.precomputed:
            if self.svd_mods is None:
                raise ValueError('please input precomputed SVD factorization dictionary')
            else:
                for mod in self.mods:
                    u_mods[mod],v_mods[mod] = self.svd_mods[mod][0], self.svd_mods[mod][1]
                    C_mods[mod],D_mods[mod] = self.prepocess_precompute(X_mods[mod],u_mods[mod],v_mods[mod])

        else:
            for mod in self.mods:
                u_mods[mod],v_mods[mod],C_mods[mod],D_mods[mod] = self.prepocess(X_mods, mod)

        while True:

            F, UU = self.fit_F(C_mods,v_mods,S_mods, G_mods, ww_mods)
            wl = {}
            loss = 0
            for mod in self.mods:
                n_f = self.n_component[mod][0]

                G_mod = self.fit_G(D_mods,u_mods,F,S_mods, mod)
                G_mods[mod] = G_mod
                S_mod = self.fit_S(X_mods,F,G_mods, mod)
                S_mods[mod] = S_mod

                UU_mod = UU[mod]
                C_mod = C_mods[mod]
                
                wl_mod, loss_mod = self.ww(F,UU_mod,C_mod)
                wl[mod] = wl_mod
                loss += loss_mod

            for mod in self.mods:
                ww_mods[mod] = wl[mod]/np.sum(list(wl.values()))

            iteration += 1
            self.loss.append(loss)
            #self.loss_atac.append(c_atac)
            #self.loss_rna.append(c_gene)
            if iteration >= self.epoch_phase_1:
                break
        
        Flag = True
        for mod in self.mods:
            ww_mod = ww_mods[mod]
            if Flag:
                    C = C_mods[mod]
                    Flag = False
            else:
                    C = np.concatenate((C,C_mods[mod]*ww_mod), axis=1)
        
        reducer = UMAP()
        embedding = reducer.fit_transform(C)
        self.embedding = embedding
        
        self.F_rough = F
        F_new = self.subcluster(F,C_mods)
        
        while True:
            loss = 0
            for mod in self.mods:
                n_f = self.n_component[mod][0]

                S_mod = self.fit_S(X_mods,F_new,G_mods, mod)
                S_mods[mod] = S_mod
                G_mod = self.fit_G(D_mods,u_mods,F_new,S_mods, mod)
                G_mods[mod] = G_mod
                
                U = S_mod@G_mod.T
                UU_mod = U@v_mods[mod].T[:,0:n_f]
                C_mod = C_mods[mod]

                wl_mod, loss_mod = self.ww(F_new,UU_mod,C_mod)
                wl[mod] = wl_mod
                loss += loss_mod

            iteration+=1
            self.loss.append(loss)

            if iteration >= self.epoch_phase_2 or np.abs(self.loss[iteration-1]-self.loss[iteration-2])<=0.1:
                break

        for mod in self.mods:
            ww_mods[mod] = wl[mod]/np.sum(list(wl.values()))


        Flag = True
        for mod in self.mods:
            ww_mod = ww_mods[mod]
            if Flag:
                    C = C_mods[mod]
                    Flag = False
            else:
                    C = np.concatenate((C,C_mods[mod]*ww_mod), axis=1)

        embedding = reducer.fit_transform(C)
        self.embedding = embedding
        

        for mod in self.mods:
            S_mod = S_mods[mod]
            S_mods[mod] = S_mod[:,S_mod.sum(axis=0)!=0]
            G_mod = G_mods[mod]
            G_mods[mod] = G_mod[:,G_mod.sum(axis=0)!=0]        
            mdata.mod[mod].var['group'] = np.argmax(G_mod.T, axis = 0).astype(str)

        self.iteration = iteration

        mdata.obsm['tritan_umap'] = self.embedding
        mdata.obs['tritan_cluster'] = np.argmax(F_new.T, axis = 0).astype(str)

        self.F = F_new
        self.S = S_mods
        self.G = G_mods
        

            
    def tfidf(self, X):
        transformer = TfidfTransformer()
        tf_idf = transformer.fit_transform(X)
        
        return tf_idf
    
    def load(self,mdata, mod):        
        X = mdata[mod].X
        m, n = X.shape
        X = self.tfidf(X)
        X = csr_matrix(X) 
        return X, m, n  
    
    def prepocess_precompute(self, X_mods, u, v, mod):
        X_mod = X_mods[mod]
        n_f, n_g = self.n_component[mod]
        C_mod = X_mod@v.T[:,0:n_f]
        D_mod = u[:,0:n_g].T@X_mod
        return C_mod, D_mod
    
    def prepocess(self,X_mods, mod):
        X_mod = X_mods[mod]
        n_f, n_g = self.n_component[mod]
        maxcom = max(self.n_component[mod])
        u_mod, s, v_mod = randomized_svd(X_mod, n_components = maxcom, random_state = 0)
        C_mod = X_mod@v_mod.T[:,0:n_f]
        D_mod = u_mod[:,0:n_g].T@X_mod

        return u_mod, v_mod, C_mod, D_mod
    
    def initialize_(self, X_mods):
        S_mods = {}
        G_mods = {}
        ww_mods = {}
        for mod in self.mods:
            X_mod = X_mods[mod]
            n_mod = self.n_features[mod]
            max_mod = X_mod.max()
            S_mod = np.random.uniform(0,max_mod,[self.resolution,self.feature_granularity])
            G_mod = np.random.uniform(0,max_mod,[n_mod,self.feature_granularity])
            S_mods[mod] = S_mod
            G_mods[mod] = G_mod
            ww_mods[mod] = 1/self.n_modalities
        return S_mods, G_mods, ww_mods
    
    def np_pearson_cor(self,x, y):
        xv = x - x.mean(axis=0)
        yv = y - y.mean(axis=0)
        xvss = (xv * xv).sum(axis=0)
        yvss = (yv * yv).sum(axis=0)
        result = np.matmul(xv.transpose(), yv) / np.sqrt(np.outer(xvss, yvss))
        # bound the values to -1 to 1 in the event of precision issues
        return np.maximum(np.minimum(result, 1.0), -1.0)
    
    def fit_F(self,C_mods,v_mods,S_mods, G_mods, ww_mods):
        m = self.n_cells
        index_m = np.array([i for i in range(m)])
        UU = {}
        F = 0
        for mod in self.mods:
            #print(mod)
            ww_mod = ww_mods[mod]
            F_mod = np.zeros([m, self.resolution])
            n_f = self.n_component[mod][0]
            C_mod, v_mod, S_mod, G_mod = C_mods[mod], v_mods[mod], S_mods[mod], G_mods[mod]
            U = S_mod@G_mod.T
            UU_mod = U@v_mod.T[:,0:n_f]
            t = cKDTree(UU_mod).query(C_mod, k = self.complexity, workers=-1)[1]
            p = self.np_pearson_cor(C_mod.T,UU_mod.T)
            z=[]
            for i in range(m):
                y =np.argmax(np.abs(p[i])[t[i]],axis=0)
                z.append(t[i][y])
            F_mod[index_m,z]=1
            UU[mod] = UU_mod
            F += ww_mod * F_mod 
        return F, UU
    
    def fit_G(self, D_mods,u_mods,F,S_mods, mod):
        D_mod, u_mod, S_mod = D_mods[mod], u_mods[mod], S_mods[mod] 
        n_g = self.n_component[mod][1]
        n_mod = self.n_features[mod]
        index_n = np.array([i for i in range(n_mod)])
        V = F@S_mod
        VV = u_mod[:,0:n_g].T@V
        G_mod = np.zeros([n_mod, self.feature_granularity])
        k = cKDTree(VV.T).query(D_mod.T, k = self.complexity, workers=-1)[1]
        p = self.np_pearson_cor(D_mod, VV)
        z=[]
        for i in range(n_mod):
            y =np.argmax(np.abs(p[i])[k[i]],axis=0)
            z.append(k[i][y])
        G_mod[index_n,z]=1
        return G_mod
    
    def fit_S(self, X_mods, F, G_mods, mod): 
        X_mod, G_mod = X_mods[mod], G_mods[mod]
        enum = np.linalg.pinv(F.T@F) 
        denom = np.linalg.pinv(G_mod.T@G_mod)
        S_mod = enum@F.T@X_mod@G_mod@denom
        return S_mod
    
    def ww(self,F, UU_mod, C_mod):
        soft_matrix = F@UU_mod
        p = C_mod - soft_matrix
        loss_mod = inner1d(p,p)
        mean_mod = np.mean(np.abs(p),axis=1)
        loss_mod = np.expand_dims(loss_mod, 1)
        mean_mod  = np.expand_dims(mean_mod, 1)
        wl_mod = mean_mod/loss_mod
        loss_mod = np.sum(loss_mod)
        return wl_mod, loss_mod   
    
    def subcluster(self, F, C_mods):
        group = np.argmax(F, axis=1)
        unique_groups = np.unique(group)
        new_labels = np.zeros(self.n_cells, dtype=int)
        total_clusters = 0

        # Mapping from old cluster labels to new unique labels
        label_mapping = {}

        for i in unique_groups:
            indices = np.where(group == i)[0]
            embedding = self.embedding[indices, :]
            clusterer = hdbscan.HDBSCAN(min_cluster_size=self.res).fit(embedding)
            labels = clusterer.labels_

            # Handle noise points and shift labels
            noise_mask = labels == -1
            unique_labels = np.unique(labels[~noise_mask])

            # Update label mapping
            for ul in unique_labels:
                total_clusters += 1
                label_mapping[ul] = total_clusters

            # Assign new labels
            labels_shifted = np.zeros_like(labels)
            labels_shifted[~noise_mask] = [label_mapping[l] for l in labels[~noise_mask]]
            # Noise points remain labeled as 0

            new_labels[indices] = labels_shifted

        # Determine the number of clusters including noise (if present)
        used_labels = np.unique(new_labels)
        rank1 = total_clusters + (1 if 0 in used_labels else 0)

        # Create one-hot encoded matrix for new labels
        F_new = np.zeros((self.n_cells, rank1), dtype=int)
        F_new[np.arange(self.n_cells), new_labels] = 1

        ii = new_labels  # Cluster assignments for each cell
        rank2 = min(v[0] for v in self.n_component.values())

        out_list = []
        UU_list = []

        for mod in self.mods:
            C_mod = C_mods[mod]
            # Cells assigned to noise (cluster 0)
            out_mod = C_mod[ii == 0, :]
            out_list.append(out_mod)

            # Compute the mean for each cluster (excluding noise)
            UU_mod = np.array([C_mod[ii == c, :].mean(axis=0) for c in range(1, rank1)])
            UU_list.append(UU_mod)

        out = np.concatenate(out_list, axis=1)
        UU = np.concatenate(UU_list, axis=1)

        # Find the nearest cluster for noise points and reassign
        t = cKDTree(UU).query(out, k=1, workers=-1)[1]
        F_new[ii == 0, t + 1] = 1  # t + 1 because clusters start from 1

        # Remove the noise column and any zero columns
        F_new = F_new[:, 1:]
        F_new = F_new[:, np.any(F_new != 0, axis=0)]

        return F_new