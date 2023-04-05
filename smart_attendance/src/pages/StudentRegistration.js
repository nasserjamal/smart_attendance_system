import React, { useState } from 'react';
import axios from 'axios';
import 'webrtc-adapter';


function StudentRegistration() {
  const [name, setName] = useState('');
  const [regNo, setRegNo] = useState('');
  const [images, setImages] = useState([]);
  const [message, setMessage] = useState('');

  const handleNameChange = (e) => {
    setName(e.target.value);
  };

  const handleRegNoChange = (e) => {
    setRegNo(e.target.value);
  };

  const handleImageChange = (e) => {
    const files = e.target.files;
    const updatedImages = [...images];

    for (let i = 0; i < files.length; i++) {
      updatedImages.push(files[i]);
    }

    setImages(updatedImages);
  };

  const handleCaptureImage = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    const track = stream.getVideoTracks()[0];
    const imageCapture = new ImageCapture(track);
    const blob = await imageCapture.takePhoto();
    const file = new File([blob], 'image.jpg', { type: 'image/jpeg' });
    const updatedImages = [...images];
    updatedImages.push(file);
    setImages(updatedImages);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();

    formData.append('name', name);
    formData.append('reg_no', regNo);

    for (let i = 0; i < images.length; i++) {
      formData.append('images', images[i]);
    }
    try{
      const response = await axios.post('http://localhost:5000/react/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
    });
    setMessage(response.data['status']);

  }catch(error){
    console.log(error);
  }

    setName('');
    setRegNo('');
    setImages([]);
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
        <button type="button" onClick={handleCaptureImage}>
          Capture Image
        </button>
        <br />
        <p id="msg">{message}</p>
        <br />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}


export default StudentRegistration;