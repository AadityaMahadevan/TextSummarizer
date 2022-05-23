function download(text, file_type,) {

 
    if (file_type == 'txt') {
        var element = document.createElement('a');
        var filename = "summary.txt";
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
        element.setAttribute('download', filename);

        element.style.display = 'none';
        document.body.appendChild(element);

        element.click();

        document.body.removeChild(element);
    }
}

document.getElementById("downloadSummaryFile").addEventListener("click", function(){

    // var downloadAs = document.getElementById("downloadAs");
    var file_type = 'txt'//downloadAs.value;
    var oneLineSummary = document.getElementById("One_Line_Summary").textContent;
    var abstractiveSummary = document.getElementById("Abstractive_Summary").textContent;
    var extractiveSummary = document.getElementById("Extractive_Summary").textContent;

    var text= 'One line summary:\n'+oneLineSummary+'Abstractive Summary:\n'+abstractiveSummary+'Extractive Summary:\n'+extractiveSummary
    download(text,file_type);
}, false);

