from sklearn import svm, metrics
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

import cv2
import numpy as np
import joblib
import cvutils
import matplotlib.pyplot as plt
from tqdm import tqdm_notebook as tqdm

#Get Training Images
ss_set = cvutils.imlist("/Users/jason/DuckieTown-Lib/vision_processing/dataset/ss_crop/")
tl_set = cvutils.imlist("/Users/jason/DuckieTown-Lib/vision_processing/dataset/tl_crop/")
neg_set = cvutils.imlist("/Users/jason/DuckieTown-Lib/vision_processing/dataset/neg_crop/")

labels = np.array([0]*len(neg_set) + [1]*len(ss_set) + [2]*len(tl_set))

img_list = []
for img in neg_set + ss_set + tl_set:
    img_list.append(cv2.imread(img,0))

# flatten 3D array to 2D
img_list = np.array(img_list)
n, x, y = img_list.shape
img_list = img_list.reshape((n, x*y))

X_train, X_test, y_train, y_test = train_test_split(img_list, labels, test_size = 0.25, random_state=0)

'''
# PLOT PRINCIPAL COMPONENTS VARIANCE
# Scale data for PCA
scaler = StandardScaler()
scaler.fit(img_list)
feature_scaled = scaler.transform(img_list)

# Apply PCA
pca = PCA(n_components=25)
pca.fit(feature_scaled)
feature_scaled_pca = pca.transform(feature_scaled)
print("shape of the scaled and PCA features: ", np.shape(feature_scaled_pca))

feat_var = np.var(feature_scaled_pca, axis=0)
feat_var_rat = feat_var/(np.sum(feat_var))
print("variance ratio of the n principal components: ", feat_var_rat)

# Plot principal components variance
per_var = np.round(pca.explained_variance_ratio_* 100, decimals=1)
labels = ['PC' + str(x) for x in range(1, len(per_var)+1)]

plt.bar(x=range(1,len(per_var)+1), height=per_var, tick_label=labels)
#plt.plot(range(1,len(per_var)+1), np.cumsum(per_var), '-ok', color='black')
plt.ylabel('Percentage of Explained Variance')
plt.xlabel('Principal Component')
plt.title('Screen Plot')
plt.show()
'''

pipeline_steps = [('scaler', StandardScaler()), ('pca', PCA()), ('SVM', svm.SVC(probability=True, decision_function_shape='ovr'))]

check_params = {
    'pca__n_components': [175],
    'SVM__kernel' : ['rbf', 'poly'],
    'SVM__C' : [0.001, 0.01, 0.1, 1, 10, 20, 30, 40, 50, 100, 500, 1000],
    'SVM__gamma': [0.0001, 0.001, 0.01, 0.1, 1, 5, 10, 50]
}
pipeline = Pipeline(pipeline_steps)
clf_grid = GridSearchCV(pipeline, param_grid=check_params, n_jobs=-1)
clf_grid.fit(X_train, y_train)

y_pred = clf_grid.predict(X_test)
print("Best Parameters:\n", clf_grid.best_params_)
print("Best Estimators:\n", clf_grid.best_estimator_)
print("Classification accuracy:\n", metrics.accuracy_score(y_test, y_pred))

joblib.dump(clf_grid, "clf")
print(confusion_matrix(y_test, y_pred))

'''
('Best Parameters:\n', {'pca__n_components': 175, 'SVM__C': 0.001, 'SVM__kernel': 'poly', 'SVM__gamma': 0.001})
('Best Estimators:\n', Pipeline(memory=None,
     steps=[('scaler', StandardScaler(copy=True, with_mean=True, with_std=True)), ('pca', PCA(copy=True, iterated_power='auto', n_components=175, random_state=None,
  svd_solver='auto', tol=0.0, whiten=False)), ('SVM', SVC(C=0.001, cache_size=200, class_weight=None, coef0=0.0,
  decision_function_shape='ovr', degree=3, gamma=0.001, kernel='poly',
  max_iter=-1, probability=True, random_state=None, shrinking=True,
  tol=0.001, verbose=False))]))
('Classification accuracy:\n', 0.99375)
'''
