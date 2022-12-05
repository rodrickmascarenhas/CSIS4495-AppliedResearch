function viewForm(formId) {
  fetch("/view-form", {
    method: "POST",
    body: JSON.stringify({ formId: formId }),
  }).then((_res) => {
    window.location.href = "/form/"+formId;
  });
}

function deleteForm(formId) {
  fetch("/delete-form", {
    method: "POST",
    body: JSON.stringify({ formId: formId }),
  }).then((_res) => {
    window.location.href = "/form";
  });
}

function sendForm(formId) {
  fetch("/send-form", {
    method: "POST",
    body: JSON.stringify({ formId: formId }),
  }).then((_res) => {
    window.location.href = "/send/"+formId;
  });
}

function getText(formId) {
  var note = document.querySelector("#notes").value;
  fetch("/add-note", {
    method: "POST",
    body: JSON.stringify({ formId:formId, note:note }),
  }).then((_res) => {
    window.location.href = "/report/"+formId+"/"+note;
  });
}