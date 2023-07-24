import React, { useState } from 'react';
import axios from 'axios';
import './App.css'

const App = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [data,setData] = useState([]);
  
  const fetchDataFromAPI = () =>{
    axios.get('http://localhost:5000/get_data')
        .then(response =>{
          setData(response.data);
        })
        
        .catch(error =>{
          console.error('Error fetching data:',error);
        });
  };
  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleFileUpload = () => {
    const formData = new FormData();
    formData.append('file', selectedFile);

    axios.post('http://localhost:5000/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    .then((response) => {
      console.log('File uploaded successfully');
    })
    .catch((error) => {
      console.error('Error uploading file:', error);
    });
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <button className='ubutton' onClick={handleFileUpload}>Upload</button>
      <button className="fbutton"onClick={fetchDataFromAPI}>Fetch Data </button>
      {data.length > 0 && (
        <table>
          <thead>
            <tr>
              <th>datetime</th>
              <th>close</th>
              <th>high</th>
              <th>low</th>
              <th>open</th>
              <th>volume</th>
              <th>instrument</th>
            </tr>
          </thead>
          <tbody>
            {data.map(item => (
              <tr key ={item.id}>
                <td>{item.datetime}</td>
                <td>{item.clase}</td>
                <td>{item.high}</td>
                <td>{item.low}</td>
                <td>{item.open}</td>
                <td>{item.vol}</td>
                <td>{item.instrument}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default App;

