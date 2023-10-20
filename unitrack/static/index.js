const notifications = document.getElementById("notifications");

const showNotification = (type, message) => {
  let className, icon, title, description, textColor;

  switch (type) {
    case "success":
      icon = `<i class="fa-solid fa-circle-check text-green-600"></i>`;
      textColor = "text-green-600";
      title = "Success!";
      description = message;
      break;

    case "error":
      icon = `<i class="fa-solid fa-circle-exclamation text-red-600"></i>`;
      textColor = "text-red-600";
      title = "Error!";
      description = message;
      break;

    case "warning":
      icon = `<i class="fa-solid fa-triangle-exclamation text-yellow-600"></i>`;
      textColor = "text-yellow-600";
      title = "Warning!";
      description = message;
      break;
  }

  const div = document.createElement("div");
  div.className = `w-full max-w-sm overflow-hidden bg-white rounded-lg shadow-lg pointer-events-auto ring-1 ring-black ring-opacity-5 ${className}`;

  div.innerHTML = `
    <div class="p-4">
      <div class="flex items-start space-x-4">
        <div class="flex space-x-4">
          <div class="flex-shrink-0">
            ${icon}
          </div>
          <div class="flex-1">
            <p class="font-medium ${textColor}">${title}</p>
            <p class="text-sm text-gray-600">${description}</p>
          </div>
        </div>
        <div class="flex flex-shrink-0">
          <button type="button"
            class="flex justify-center items-center text-gray-600 w-5 h-5 bg-white rounded-md hover:text-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:ring-offset-2">
           <i class="fa-solid fa-xmark"></i>
          </button>
        </div>
      </div>
  </div>`;

  div.querySelector("button").onclick = () => {
    notifications.removeChild(div);
  };

  notifications.appendChild(div);

  setTimeout(() => {
    notifications.removeChild(div);
  }, 3000);
};
