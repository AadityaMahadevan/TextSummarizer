function download(text, file_type,) {

    if (file_type == 'txt') {
        var element = document.createElement('a');
        var filename = "transcript.txt";
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
        element.setAttribute('download', filename);

        element.style.display = 'none';
        document.body.appendChild(element);

        element.click();

        document.body.removeChild(element);
    }
    
}

document.getElementById("downloadTranscriptFile").addEventListener("click", function(){

    //var downloadAs = document.getElementById("downloadAs");
    var file_type = 'txt'//downloadAs.value;
    var text = document.getElementById("TranscriptContent").textContent;
    download(text,file_type);
}, false);




// import { Document, Packer, Paragraph, HeadingLevel } from "docx";
// import { saveAs } from "file-saver";

// function saveDocumentToFile(doc, fileName) {
//   // Create new instance of Packer for the docx module

//   // Create a mime type that will associate the new file with Microsoft Word
//   const mimeType =
//     "application/vnd.openxmlformats-officedocument.wordprocessingml.document";
//   // Create a Blob containing the Document instance and the mimeType
//   Packer.toBlob(doc).then((blob) => {
//     const docblob = blob.slice(0, blob.size, mimeType);
//     // Save the file using saveAs from the file-saver package
//     saveAs(docblob, fileName);
//   });
// }

// function generateWordDocument(event) {
//   event.preventDefault();
//   // Create a new instance of Document for the docx module
//   let doc = new Document({   
//     sections: [
//       {
//         children: [
//           new Paragraph({ text: text}),          
//         ]
//       }
//     ]
//   });
//   // Call saveDocumentToFile with the document instance and a filename
//   saveDocumentToFile(doc, "New Document.docx");
// }

// // Listen for clicks on Generate Word Document button
// document.getElementById("generate").addEventListener(
//   "click",
//   function (event) {
//     generateWordDocument(event);
//   },
//   false
// );

//   // Start file download.
