import urlFeatures
import jsFeatures
import domainFeatures
import pickle
import numpy as np

url = "https://poczta-order.pl-id69822218.xyz"

features = []
features.extend(urlFeatures.fetchURLFeatures(url))
features.extend(jsFeatures.fetchJSFeatures(url))
features.extend(domainFeatures.fetchDomainFeatures(url))

print(features)

features = np.array(features)
features = features.reshape(1, -1)

filename = 'model.sav'
loaded_model = pickle.load(open(filename, 'rb'))
result = loaded_model.predict(features)
print(result)
