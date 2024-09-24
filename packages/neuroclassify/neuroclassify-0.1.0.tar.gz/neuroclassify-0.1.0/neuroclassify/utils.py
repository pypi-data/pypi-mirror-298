import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image

def load_and_preprocess_image(img_path, target_size=(150, 150)):
    """Load and preprocess the image."""
    try:
        img = image.load_img(img_path, target_size=target_size)  # Resize to match model input
        img_array = image.img_to_array(img)  # Convert to array
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        img_array = img_array / 255.0  # Rescale to [0, 1]
        return img_array
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

def predict_image(model, img_path, class_labels, img_size=(150, 150)):
    """Predict the class of an image and display the result."""
    img_array = load_and_preprocess_image(img_path, target_size=img_size)
    if img_array is None:
        return None, None  # Exit if image loading failed

    predictions = model.predict(img_array)  # Get predictions
    predicted_class = np.argmax(predictions, axis=1)[0]
    predicted_class_name = class_labels[predicted_class]
    predicted_probabilities = predictions[0]  # Get probabilities for all classes

    # Display the image
    img = image.load_img(img_path)
    plt.imshow(img)
    plt.title(f'Predicted: {predicted_class_name}\nProbabilities: {predicted_probabilities}')
    plt.axis('off')
    plt.show()

    return predicted_class_name, predicted_probabilities

def predict_images(model, img_dir, class_labels, img_size=(150, 150)):
    """Predict classes for all images in a directory."""
    predictions = []
    
    # Iterate through all image files in the directory
    for filename in os.listdir(img_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            img_path = os.path.join(img_dir, filename)
            predicted_class_name, predicted_probabilities = predict_image(model, img_path, class_labels, img_size)
            predictions.append((filename, predicted_class_name, predicted_probabilities))
    
    return predictions
