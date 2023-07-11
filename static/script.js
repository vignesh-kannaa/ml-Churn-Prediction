window.addEventListener("load", function () {
  toggleBulkOption(false);
  bulkOption.style.display = "none";
});
// ------------toggle function----------------
function toggleBulkOption(value) {
  document.getElementById("resultimg").src = "static/hit.gif";
  document.getElementById("result").innerHTML = "";
  var bulkOption = document.getElementById("bulkOption");
  var singleOptions = document.getElementsByName("singleOption");
  if (value === "false") {
    bulkOption.style.display = "none";
    for (var i = 0; i < singleOptions.length; i++) {
      singleOptions[i].style.display = "block";
    }
  }
  if (value === "true") {
    bulkOption.style.display = "block";
    for (var i = 0; i < singleOptions.length; i++) {
      singleOptions[i].style.display = "none";
    }
  }
}
document
  .getElementById("forminput")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent form from submitting
    var form = document.getElementById("forminput");
    var formdata = new FormData(form);
    var toggleCheckbox = document.getElementById("fileType");
    if (toggleCheckbox.checked) {
      sendBulkData(formdata);
    } else {
      sendData(formdata);
    }
  });

function sendBulkData(data) {
  fetch("/predictBulkData", {
    method: "POST",
    body: data,
  })
    .then((response) => response.text())
    .then((result) => {
      document.getElementById("result").innerHTML = result;
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
function sendData(data) {
  fetch("/predictData", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(Object.fromEntries(data)),
  })
    .then((response) => response.json())
    .then((result) => {
      document.getElementById("result").innerHTML = result[0];
      document.getElementById("resultimg").src = "static/" + result[1];
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
