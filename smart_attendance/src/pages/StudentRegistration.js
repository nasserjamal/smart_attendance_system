import React, { useState } from 'react';
import axios from 'axios';
import 'webrtc-adapter';
import './StudentRegistration.css'


function StudentRegistration() {
  const [errorMessages, setErrorMessages] = useState('');
  const [name, setName] = useState('');
  const [regNo, setRegNo] = useState('');
  const [images, setImages] = useState([]);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);


  const validateForm = () => {
    let errors = [];
    let isValid = true;

    if (name.trim() === '') {
      errors.push('Name is required.');
      isValid = false;
    }

    if (regNo.trim() === '') {
      errors.push('Registration No is required.');
      isValid = false;
    }

    if (images.length < 5) {
      errors.push('At least 5 images must be uploaded.');
      isValid = false;
    }

    setErrorMessages(errors.join(' '));
    return isValid;
  };

  const handleNameChange = (e) => {
    setName(e.target.value);
  };

  const handleRegNoChange = (e) => {
    setRegNo(e.target.value);
  };

  const handleImageChange = async (e) => {
    const files = e.target.files;
    setErrorMessages('');
  
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const imageDataUrl = await readFileAsDataURL(file);
  
      const result = await sendImageToServer(imageDataUrl);
      if (result) {
        setImages((prevImages) => [...prevImages, file]);
      } else {
        setErrorMessages((prevErrorMessages) => prevErrorMessages + 'Error! Could not process image: ' + file.name + '\n');
      }
    }
  };

  const handleDeleteImage = (imageToDelete) => {
    setImages((prevImages) => prevImages.filter((image) => image !== imageToDelete));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    const formData = new FormData();

    formData.append('name', name);
    formData.append('reg_no', regNo);

    for (let i = 0; i < images.length; i++) {
      formData.append('images', images[i]);
    }

    setLoading(true);
    try{
      const response = await axios.post('http://192.168.20.42:5000/react/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
    if(response.status === 200){
      setMessage(response.data['status']);
      setName('');
      setRegNo('');
      setImages([]);
    } else if (response.status === 400) {
      console.log('Error status code:', response.status);
      console.log('Error message:', response.data.error);
    } else {
      console.log('Request was not successful. Status code:', response.status);
    }

    }catch(error){
      if (error.response) {
        // The request was made and the server responded with a status code that falls out of the range of 2xx
        console.log('Error status code:', error.response.status);
        console.log('Error message:', error.response.data.error);
        setErrorMessages(error.response.data.error)
      } else if (error.request) {
        // The request was made but no response was received
        console.log('No response received:', error.request);
        setErrorMessages("Error! No response received from the server:", error.request)
      } else {
        // Something happened in setting up the request that triggered an Error
        console.log('Error', error.message);
      }
      setLoading(false);
    }
    setLoading(false);
  };

  const readFileAsDataURL = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onloadend = () => {
        resolve(reader.result);
      };
      reader.onerror = () => {
        reject(reader.error);
      };
      reader.readAsDataURL(file);
    });
  };

  const sendImageToServer = async (imageDataUrl) => {
    try {
      const response = await axios.post('http://192.168.20.42:5000/react/image_check', {
        image: imageDataUrl,
      });
      return response.data.valid;
    } catch (error) {
      console.error('Error sending image to server:', error);
      return false;
    }
  };
  
  

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>
          Name:
          <input type="text" value={name} onChange={handleNameChange} />
        </label>
        <br />
        <label>
          Registration No:
          <input type="text" value={regNo} onChange={handleRegNoChange} />
        </label>
        <br />
        <label>
          Upload Images:
          <input type="file" accept="image/*" multiple onChange={handleImageChange} />
        </label>
        <br />
        
        <p id="msg">{message}</p>
        <br />

        <div className="image-container">
      {images.map((image, index) => (
        <div key={index} className="image-wrapper">
          <div className='image-class'>
            <img src={URL.createObjectURL(image)} alt={`Uploaded img ${index}`} />
          </div>
          <p>{image.name}</p>
          <button className="delete-button" onClick={() => handleDeleteImage(image)}>Delete</button>
        </div>
      ))}
    </div>

    <div>
      <p className="error-message">{errorMessages}</p>
    </div>
        
    {loading ? (
          <div className="spinner">Loading...</div>
        ) : (
          <button type="submit">Submit</button>
        )}
      </form>


    </div>
  );
}


export default StudentRegistration;