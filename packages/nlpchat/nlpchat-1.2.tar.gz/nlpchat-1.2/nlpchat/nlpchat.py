from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras import layers, models
import pickle
import random

class NlpChat:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.classifier_lr = LogisticRegression()
        self.label_encoder = LabelEncoder()
        self.intents = []
        self.nn_model = None  # Neural network will be initialized later

    def add_intent(self, tag, patterns, responses):
        self.intents.append({
            'tag': tag,
            'patterns': patterns,
            'responses': responses
        })

    def build_nn_model(self, input_shape, num_classes):
        """Builds a simple neural network for intent classification."""
        model = models.Sequential()
        model.add(layers.InputLayer(input_shape=(input_shape,)))
        model.add(layers.Dense(128, activation='relu'))
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dense(num_classes, activation='softmax'))
        
        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        
        return model

    def train(self):
        sentences = []
        labels = []

        for intent in self.intents:
            for pattern in intent['patterns']:
                sentences.append(pattern)
                labels.append(intent['tag'])

        # Encode the labels
        encoded_labels = self.label_encoder.fit_transform(labels)

        # Convert sentences to embeddings
        sentence_embeddings = self.model.encode(sentences)

        # Split the data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(sentence_embeddings, encoded_labels, test_size=0.2, random_state=42)

        # Train Logistic Regression model
        self.classifier_lr.fit(X_train, y_train)
        
        # Build and train the Neural Network model
        num_classes = len(set(encoded_labels))
        self.nn_model = self.build_nn_model(X_train.shape[1], num_classes)
        self.nn_model.fit(X_train, y_train, epochs=10, batch_size=8, validation_data=(X_test, y_test))
        
        # Evaluate Logistic Regression
        lr_acc = self.classifier_lr.score(X_test, y_test)
        print(f"Logistic Regression Test Accuracy: {lr_acc * 100:.2f}%")

        # Evaluate Neural Network
        nn_loss, nn_acc = self.nn_model.evaluate(X_test, y_test)
        print(f"Neural Network Test Accuracy: {nn_acc * 100:.2f}%")

    def get_response(self, user_input):
        # Encode the new sentence
        embedding = self.model.encode([user_input])
        
        # Get predictions from both models
        lr_pred = self.classifier_lr.predict(embedding)
        nn_pred = np.argmax(self.nn_model.predict(embedding), axis=-1)
        
        # Ensemble by majority voting (or any other strategy)
        final_pred = random.choice([lr_pred[0], nn_pred[0]])
        
        predicted_intent = self.label_encoder.inverse_transform([final_pred])[0]

        # Find the corresponding response
        for intent in self.intents:
            if intent['tag'] == predicted_intent:
                return np.random.choice(intent['responses'])

    def get_intent(self, user_input):
        # Encode the new sentence
        embedding = self.model.encode([user_input])
        
        # Get predictions from both models
        lr_pred = self.classifier_lr.predict(embedding)
        nn_pred = np.argmax(self.nn_model.predict(embedding), axis=-1)
        
        # Ensemble by majority voting (or any other strategy)
        final_pred = random.choice([lr_pred[0], nn_pred[0]])
        
        predicted_intent = self.label_encoder.inverse_transform([final_pred])[0]
        
        return predicted_intent

    def save_model(self, filename):
        # Save the Logistic Regression model, label encoder, and neural network weights
        with open(filename, 'wb') as f:
            pickle.dump((self.classifier_lr, self.label_encoder, self.intents), f)
        self.nn_model.save(f"{filename}_nn.h5")

    def load_model(self, filename):
        # Load the Logistic Regression model, label encoder, and neural network weights
        with open(filename, 'rb') as f:
            self.classifier_lr, self.label_encoder, self.intents = pickle.load(f)
        self.nn_model = models.load_model(f"{filename}_nn.h5")
