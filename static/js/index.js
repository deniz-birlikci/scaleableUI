function add_to_table(defaults=false) {
    // Get the values from input fields
    if (defaults == false) {
        var browserValue = document.getElementById('browser').value;
        var widthValue = document.getElementById('width').value;
        var heightValue = document.getElementById('height').value;
        console.log(browserValue, widthValue, heightValue);
    } else {
        var browserValue = 'Chrome';
        var widthValue = 400
        var heightValue = 800
        console.log(browserValue, widthValue, heightValue);
    }

    // Get the table by ID
    var table = document.getElementById('tab');

    // Create a new row and cells
    var newRow = table.insertRow(-1); // -1 means add at the end of the table
    var browserCell = newRow.insertCell(0);
    var widthCell = newRow.insertCell(1);
    var heightCell = newRow.insertCell(2);
    var blank_cell = newRow.insertCell(3);
    var blank_cell = newRow.insertCell(4);
    var blank_cell = newRow.insertCell(5);
    var blank_cell = newRow.insertCell(6);
    var buttonCell = newRow.insertCell(7);

    // Add the values to the cells
    browserCell.innerHTML = browserValue;
    widthCell.innerHTML = widthValue;
    heightCell.innerHTML = heightValue;

    // Create a button and add it to the fourth cell
    var button = document.createElement('button');
    button.innerHTML = 'View'; // or any text you want on the button
    button.classList.add('btn', 'btn-light'); // Add classes to the button
    button.onclick = function() {
        // set modal-img's src to browser_width_height.png
        var modal_img = document.getElementById('modal-img');
        modal_img.src = 'https://s3.us-west-1.wasabisys.com/hackathon/' + browserValue.toLowerCase() + '_' + widthValue + '_' + heightValue + '.png';
    };
    // data-bs-toggle="modal" data-bs-target="#exampleModal"
    button.setAttribute('data-bs-toggle', 'modal');
    button.setAttribute('data-bs-target', '#exampleModal');

    // delete button
    var delete_button = document.createElement('button');
    delete_button.innerHTML = 'x'; // or any text you want on the button
    delete_button.classList.add('btn', 'btn-danger'); // Add classes to the button
    delete_button.onclick = function() {
        var row = this.parentNode.parentNode;
        row.parentNode.removeChild(row);
    };

    buttonCell.appendChild(button);
    buttonCell.appendChild(delete_button);
}

function send_data() {

    // disable button id="validate"
    document.getElementById('validate').disabled = true;

    let endpoint = '/process_data'; // Replace with your actual endpoint
    let url = document.getElementById('url').value;
    let table = document.getElementById('tab');

    let data = {
        url: url,
        configurations: []
    };

    // Collect data from the table
    for (let i = 0; i < table.rows.length; i++) {
        let row = table.rows[i];
        let browser = row.cells[0].innerHTML;
        let width = row.cells[1].innerHTML;
        let height = row.cells[2].innerHTML;

        data.configurations.push({
            browser: browser,
            width: parseInt(width),
            height: parseInt(height)
        });
    }
    // Send the data using fetch API
    console.log(data.configurations)
    fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(responseData => {
        for (let i = 0; i < responseData.length; i++) {
            let status = responseData[i];
            let row = table.rows[i]; // Adjust for header row
    
            // Update the row based on the response
            console.log(status)
            updateCellWithPopover(row.cells[3], status['Navigation'][0], status['Navigation'][1]);
            updateCellWithPopover(row.cells[4], status['Aesthetics'][0], status['Aesthetics'][1]);
            updateCellWithPopover(row.cells[5], status['Usability'][0], status['Usability'][1]);
            updateCellWithPopover(row.cells[6], status['Consistency'][0], status['Consistency'][1]);
        }
        document.getElementById('validate').disabled = false;
    })
    .catch((error) => {
        console.error('Error:', error);
        document.getElementById('validate').disabled = false;
    });
}

function updateCellWithPopover(cell, score, message) {
    cell.innerHTML = score;

    // Attach hover event
    cell.onmouseover = function() {
        // Show popover
        var popover = document.getElementById('popover');
        popover.innerHTML = message; // Set the message in the popover
        popover.style.display = 'block';
        var cell_position = cell.getBoundingClientRect();
        popover.style.left = cell_position.left-250 + 'px';
        popover.style.top = (cell_position.bottom-60) + 'px';
    };

    cell.onmouseout = function() {
        // Hide popover
        document.getElementById('popover').style.display = 'none';
    };
}


// on window load
window.onload = function() {
    add_to_table(true);
};



document.addEventListener('DOMContentLoaded', function () {
    var hoverText = document.getElementById('hoverText');
    var popover = document.getElementById('popover');

    hoverText.addEventListener('mouseover', function () {
        popover.style.display = 'block';
        var rect = hoverText.getBoundingClientRect();
        popover.style.left = rect.left + 'px';
        popover.style.top = (rect.bottom + 5) + 'px';
    });

    hoverText.addEventListener('mouseout', function () {
        popover.style.display = 'none';
    });
});
