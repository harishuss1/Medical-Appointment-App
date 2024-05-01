"use strict";
!(function(){
    function downloadPDF() {
        console.log("hello");
        const attachements = document.getElementById("download-attachements").getAttribute("data-attachements");
        for (var attachement of attachements)
        {
            const a = document.createElement('a');
            a.href = `data:application/pdf;base64,{{ ${attachement} | safe }}`;
            const words = attachement.split('/');
            var filename = words[words.length - 1]
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            a.remove();
        }
    }

    document.addEventListener("DOMContentLoaded", function(e)
    {
        document.getElementById("download-attachements").addEventListener("click", downloadPDF);
    });

}());