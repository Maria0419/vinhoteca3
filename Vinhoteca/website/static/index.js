function deleteVinho(vinhoId) {
  fetch("/delete-vinho", {
    method: "POST",
    body: JSON.stringify({ vinhoId: vinhoId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
