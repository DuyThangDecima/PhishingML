import pandas
from db.mongo import UrlTrainModel
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix

class Train():
    def test(self):
        data_file = pandas.read_csv(
            "../data/attr_classify.csv",
            names=  [
                UrlTrainModel.LEN_URL,
                UrlTrainModel.IS_SPEC_URL,
                UrlTrainModel.IS_UNI_SUB,
                UrlTrainModel.NUM_A,
                UrlTrainModel.NUM_A_NULL,
                UrlTrainModel.NUM_IMG,
                UrlTrainModel.HOST_SIMILAR,
                UrlTrainModel.IS_TITLE_KW,
                UrlTrainModel.LEN_TXT_VIS,
                UrlTrainModel.TXT_SIMILAR,
                UrlTrainModel.NUM_TXT_KW,
                UrlTrainModel.SIZE_RES,
                UrlTrainModel.NUM_DOMAIN_PROTECT,
                UrlTrainModel.TYPE
            ]
        )
        X = data_file.drop(UrlTrainModel.TYPE, axis=1)
        y = data_file[UrlTrainModel.TYPE]
        X_train, X_test, y_train, y_test = train_test_split(X, y)
        scaler =StandardScaler()
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)
        mlp = MLPClassifier()
        mlp.fit(X_train,y_train)
        predictions = mlp.predict(X_test)
        print predictions

        print (confusion_matrix(y_test, predictions))
        print classification_report(y_test, predictions)


train = Train()
train.test()