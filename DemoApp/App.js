import React, { Component, useState } from 'react'
import { View, Text, StyleSheet, Button, Image, ScrollView } from 'react-native'
import { launchImageLibrary } from 'react-native-image-picker'
import * as FS from 'expo-file-system'
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
    const [clicked, setClicked] = useState(false)
    const toServer = async (mediaFile) => {
        let type = mediaFile.type;
        let schema = "http://";
        let host = "localhost";
        let route = "/image";
        let port = "5000";
        let url = "";
        let content_type = "image/jpg";

        url = schema + host + ":" + port + route;
    
        let response = await FS.uploadAsync(url, mediaFile.uri, {
          headers: {
            "content-type": content_type,
          },
          httpMethod: "POST",
          uploadType: FS.FileSystemUploadType.BINARY_CONTENT,
        });
    
        console.log(response.headers);
        console.log(response.body);
      };
    
    const chooseFile = async () => {
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
          if (response.assets[0].type == "image") {
            toServer({
              type: response.assets[0].type,
              base64: response.assets[0].base64,
              uri: response.assets[0].uri,
            });
          } else {
            let base64 = uriToBase64(response.assets[0].uri);
            toServer({
              type: response.assets[0].type,
              base64: base64,
              uri: response.assets[0].uri,
            });
          }
        })
      setClicked(true)
    }

    const uriToBase64 = async (uri) => {
        let base64 = await FS.readAsStringAsync(uri, {
          encoding: FS.EncodingType.Base64,
        });
        return base64;
      };

    return (
      <View style={styles.Container}>
        <Text style={styles.topTitle}>CS232 Demo App</Text>
        <ScrollView 
          // style={{justifyContent: 'center'}}
          contentContainerStyle={styles.contentContainer}>
          <View style={{paddingBottom: 10, justifyContent: 'center', alignSelf: 'center'}}>
            <Button color='#290' title="Upload" onPress={() => chooseFile()} />
          </View>
            {PHOTO_uri &&
              <Image
                source={{ uri: PHOTO_uri }}
                style={styles.mainPhoto}
              />
            }
            {clicked &&
              <View style={styles.x1}>
               <Text style={{ fontSize: 24, fontWeight: 'bold', color: '#000'}}>PREDICTION</Text>
              </View>
            }
            {clicked &&
              <View style={{justifyContent: 'space-evenly'}}>
                <Image source={require('./output/1.png')} style={styles.Photo} />
                <Image source={require('./output/2.png') } style={styles.Photo}/>
                <Image source={require('./output/3.png') } style={styles.Photo}/>
                <Image source={require('./output/4.png') } style={styles.Photo}/>
                <Image source={require('./output/5.png') } style={styles.Photo}/>
                <Image source={require('./output/6.png') } style={styles.Photo}/>
                <Image source={require('./output/7.png') } style={styles.Photo}/>
                <Image source={require('./output/8.png') } style={styles.Photo}/>
                <Image source={require('./output/9.png') } style={styles.Photo}/>
                <Image source={require('./output/10.png')} style={styles.Photo}/>
                <Image source={require('./output/11.png')} style={styles.Photo}/>
                <Image source={require('./output/12.png')} style={styles.Photo}/>
                <Image source={require('./output/13.png')} style={styles.Photo}/>
                <Image source={require('./output/14.png')} style={styles.Photo}/>
                <Image source={require('./output/15.png')} style={styles.Photo}/>
              </View>
            }
        </ScrollView>
      </View>
    );
}

const styles = StyleSheet.create({
    Container:{
        // flex: 1,
        justifyContent: 'center',
        height: '100%',
        width: '100%',
        alignItems: 'center',
        // paddingTop: 10
        backgroundColor: '#ffffff'
    },

    x1:{
      fontSize: 20,
      paddingTop: 20,
      paddingBottom: 20,
    },
    topTitle: {
      fontSize: 24,
      paddingTop: 10,
      paddingBottom: 10,
      fontWeight: 'bold',
      backgroundColor: '#03a9f4',
      color: "white",
      width: '100%',
      textAlign: 'center',
    },
    contentContainer:{
      alignItems: 'center',
      textDecorationColor: '#000',
      justifyContent: 'center',
      padding: 10,
      // paddingVertical: 10,
      flexGrow: 1,
      // backgroundColor: 'green',
    },
    Photo: {
        width: 300,
        height: 300,
        paddingBottom: 20
    },
    mainPhoto: {
      paddingBottom: 20,
      // flexGrow:1,
      height:300,
      width:300,
      alignItems: 'center',
      justifyContent:'center',
    }
})