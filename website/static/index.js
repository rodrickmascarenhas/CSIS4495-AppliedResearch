function deleteForm(formId) {
  fetch("/delete-form", {
    method: "POST",
    body: JSON.stringify({ formId: formId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
