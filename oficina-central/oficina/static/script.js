document.addEventListener("DOMContentLoaded", function () {
  var filtro = document.querySelector("form select[name='status']");
  if (filtro) {
    filtro.addEventListener("change", function () {
      filtro.form.submit();
    });
  }
});