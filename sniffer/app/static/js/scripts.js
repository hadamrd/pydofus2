var socket = io(); // This line should be at the top of your scripts.js file

document.addEventListener('DOMContentLoaded', function() {
    // Check sniffer status and update button
    fetch('/sniffer_status')
    .then(response => response.json())
    .then(data => {
        const button = document.getElementById('toggle-btn');
        if (data.sniffer_status === "running") {
            button.textContent = "Stop Sniffer";
            button.classList.add("button-red");
        } else {
            button.textContent = "Start Sniffer";
            button.classList.remove("button-red");
        }
    });

    document.getElementById('toggle-btn').addEventListener('click', toggleSniffer);
});

function toggleSniffer() {
    const button = document.getElementById('toggle-btn');
    fetch('/toggle_sniffer', {
        method: 'POST',
    }).then(response => response.json())
    .then(data => {
        alert(data.message); // Notify the user about the action
        if (data.status === "success") {
            if (data.action === "started") {
                button.textContent = "Stop Sniffer";
                button.classList.add("button-red");
            } else {
                button.textContent = "Start Sniffer";
                button.classList.remove("button-red");
            }
        }
    });
}

socket.on('connect', function() {
    console.log('Socket connected.');
});


socket.on('new_message', function(data) {
    // Handle new message
    // Update the messages in the tab corresponding to data.conn_id
    updateMessageDisplay(data.conn_id, data.message, data.from_client);
});

socket.on('sniffer_crash', function(data) {
    // Handle sniffer crash
    // Display the error message to the user
    alert("Sniffer crashed: " + data.error);
});

function sendSnifferCommand(url) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            if(response.success) {
                console.log('Sniffer command successful');
                // Update UI or perform other actions based on success
            } else {
                console.error('Sniffer command failed');
                // Handle failure
            }
        }
    };
    xhr.send(JSON.stringify({}));
}

function updateMessageDisplay(connId, message, fromClient) {
    var tabContentDiv = document.getElementById('tab-content-' + connId);
    if (!tabContentDiv) {
        createNewTab(connId);
        tabContentDiv = document.getElementById('tab-content-' + connId);
    }
    var contentBody = tabContentDiv.querySelector('.tab-content-body');
    appendMessageToTab(contentBody, message, fromClient);
}

function createNewTab(connId) {
    const tabLabelsContainer = document.getElementById('tab-labels-container');
    const tabContainer = document.getElementById('tab-container');
    const isFirstTab = tabLabelsContainer.children.length === 0; // Check if it's the first tab

    // Create the tab label with a close button using template literals for clarity
    const tabLabel = document.createElement('li');
    tabLabel.className = 'tab-label';
    tabLabel.dataset.target = `tab-content-${connId}`;
    const labelContent = document.createTextNode(connId);
    const closeButton = document.createElement('span');
    closeButton.className = 'tab-close-button';
    closeButton.textContent = '×';
    tabLabel.appendChild(labelContent);
    tabLabel.appendChild(closeButton);
    tabLabelsContainer.appendChild(tabLabel);

    // Create the tab content with a clear content button
    const tabContentDiv = document.createElement('div');
    tabContentDiv.id = `tab-content-${connId}`;
    tabContentDiv.className = 'tab-content';
    tabContainer.appendChild(tabContentDiv);

    // Create a clear content button
    const clearButton = document.createElement('button');
    clearButton.textContent = 'Clear Content';
    clearButton.className = 'clear-content-button';
    clearButton.addEventListener('click', () => {
        const contentBody = tabContentDiv.querySelector('.tab-content-body');
        if (contentBody) {
            contentBody.innerHTML = '';
        }
    });
    tabContentDiv.appendChild(clearButton);

    // Add a div for the tab content body
    const contentBody = document.createElement('div');
    contentBody.className = 'tab-content-body';
    tabContentDiv.appendChild(contentBody);

    // Toggle display based on whether it's the first tab
    tabContentDiv.style.display = isFirstTab ? 'block' : 'none';
    if (isFirstTab) {
        tabLabel.classList.add('active');
    }

    // Handling tab and close button clicks
    tabLabel.addEventListener('click', function(event) {
        // Handle close button click within the tab label
        if (event.target.classList.contains('tab-close-button')) {
            tabLabelsContainer.removeChild(tabLabel);
            tabContainer.removeChild(tabContentDiv);
            // Optionally, set another tab as active if this was the active tab
            if (tabLabel.classList.contains('active') && tabLabelsContainer.children.length > 0) {
                tabLabelsContainer.children[0].click(); // Activate the first tab
            }
            return;
        }

        // Tab activation logic
        activateTab(this.dataset.target);
    });
}

// Function to activate a tab by its content ID
function activateTab(targetId) {
    const contents = document.querySelectorAll('.tab-content');
    const labels = document.querySelectorAll('.tab-label');

    // Hide all contents and remove active class from labels
    contents.forEach(content => content.style.display = 'none');
    labels.forEach(label => label.classList.remove('active'));

    // Show the clicked tab content and set label as active
    document.getElementById(targetId).style.display = 'block';
    document.querySelector(`[data-target="${targetId}"]`).classList.add('active');
}

function appendMessageToTab(tabContentDiv, msg, fromClient) {
    // console.log('Appending message to tab:', msg);
    var messageContainer = document.createElement('div');
    messageContainer.className = 'message-container';
    messageContainer.style.display = 'flex';
    messageContainer.style.alignItems = 'center';
    messageContainer.style.justifyContent = 'space-between';

    var messageContentDiv = document.createElement('div');

    var toggleLabel = document.createElement('label');
    toggleLabel.className = 'message-toggle';
    toggleLabel.textContent = msg['__receptionTime__'] + '  -  ' + msg['__type__'];
    toggleLabel.style.color = fromClient ? '#28a745' : '#007bff'; // Green if from client, Blue otherwise

    var detailsDiv = document.createElement('div');
    detailsDiv.className = 'message-details';
    delete msg['__type__'];
    delete msg['__receptionTime__'];
    delete msg['__direction__'];
    detailsDiv.textContent = JSON.stringify(msg, null, 2);
    detailsDiv.style.display = 'none'; // Initially hide details

    toggleLabel.onclick = function() {
        detailsDiv.style.display = detailsDiv.style.display === 'none' ? 'block' : 'none';
    };

    // Create a delete button with a trash icon
    var deleteButton = document.createElement('button');
    deleteButton.className = 'delete-message';
    deleteButton.innerHTML = '<i class="fa fa-trash-o" aria-hidden="true"></i>'; // Using FontAwesome icon
    deleteButton.style.fontSize = '1.5em'; // Increase the font size for better visibility
    deleteButton.style.color = '#dc3545'; // Optional: color for the delete button
    deleteButton.style.marginLeft = '10px'; // Add some space around the button
    deleteButton.style.background = 'none';
    deleteButton.style.border = 'none';
    deleteButton.style.cursor = 'pointer';

    // Append elements to message content div
    messageContentDiv.appendChild(toggleLabel);
    messageContentDiv.appendChild(detailsDiv);

    // Append message content and delete button to the message container
    messageContainer.appendChild(messageContentDiv);
    messageContainer.appendChild(deleteButton);

    // Add functionality to delete the message
    deleteButton.onclick = function() {
        messageContainer.remove();
    };

    // Insert the message container at the top
    tabContentDiv.insertBefore(messageContainer, tabContentDiv.firstChild);
}
