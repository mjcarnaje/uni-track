function setAsyncPhotoInput(photo) {
  fetchPhoto(photo).then((file) => {
    setPhotoInput(file);
  });
}

function fetchPhoto(photo) {
  return fetch(`/uploads/${photo}`)
    .then((response) => response.blob())
    .then((blob) => new File([blob], photo, { type: blob.type }));
}

function setPhotoInput(file) {
  const photoInput = document.querySelector('input[name="photo"]');
  const fileList = fileListFrom([file]);
  photoInput.files = fileList;
  photoInput.dispatchEvent(new Event("change"));
}

function fileListFrom(files) {
  const clipboardData =
    new ClipboardEvent("").clipboardData || new DataTransfer();
  for (const file of files) {
    clipboardData.items.add(file);
  }
  return clipboardData.files;
}
