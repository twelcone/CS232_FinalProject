import React, { Component, useState } from 'react'
import { View, Text, StyleSheet, Button, Image } from 'react-native'
import { launchImageLibrary } from 'react-native-image-picker'
import axios from 'axios'

const options={
    title: 'Select Image',
    type: 'library',
    options: {
        maxHeight: 300,
        maxWidth: 300,
        selectionLimit: 1,
        mediaType: "photo",
        includeBase64: true,
    },
}
export default function App() {
    const [filePath, setFilePath] = useState({})
    const [PHOTO_uri, setPHOTO_uri] = useState(null)
    const [PHOTO_64, setPHOTO_64] = useState(null)

    
    const chooseFile = () => {
        let options = {
          mediaType: 'photo',
          maxWidth: 300,
          maxHeight: 550,
          quality: 1,
        };
        launchImageLibrary(options, (response) => {
          console.log('Response = ', response);
     
          if (response.didCancel) {
            alert('User cancelled camera picker');
            return;
          } else if (response.errorCode == 'camera_unavailable') {
            alert('Camera not available on device');
            return;
          } else if (response.errorCode == 'permission') {
            alert('Permission not satisfied');
            return;
          } else if (response.errorCode == 'others') {
            alert(response.errorMessage);
            return;
          }
          console.log('base64 -> ', response.assets[0].base64);
          console.log('uri -> ', response.assets[0].uri);
          console.log('width -> ', response.assets[0].width);
          console.log('height -> ', response.assets[0].height);
          console.log('fileSize -> ', response.assets[0].fileSize);
          console.log('type -> ', response.assets[0].type);
          console.log('fileName -> ', response.assets[0].fileName);
          setFilePath(response);
          setPHOTO_uri(response.assets[0].uri)
          console.log(filePath)
        });
    };

    const predictImage=async()=>{ 
        const image = PHOTO_uri

        const formdata= new FormData()
        // formdata.append('name', 'Upload Image')
        formdata.append('file', image)

        let res = await fetch(
            "http://127.0.0.1:5000/predict",
            {
                method: 'POST',
                body: formdata,
            }
        );
        let response = await res;
        console.log(response)
        // let responseJson = await res.json();
        // if (responseJson.status == 1) {
        //     alert('Upload Successful');
        //   } else {
        //   //if no file selected the show alert
        //   alert('Please Select File first');
        // }
    }
    // const formdata=new FormData()
    // formdata.append('file', images.assets[0].uri)
    return (
        <View style={styles.Container}>
            <Button title="Upload" onPress={() => chooseFile()}></Button>
            <Image
                source={{ uri: PHOTO_uri }}
                style={styles.Photo}
            />
            <Button title="Predict" onPress={predictImage}></Button>
        </View>
    );
}

const styles = StyleSheet.create({
    Container:{
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center'
    },
    Photo: {
        width: 300,
        height: 300
    },
})