const rooms = [];

function generateDesksForm() {
    const newRoomName = document.getElementById('newRoomName').value;
    const newNumDesks = document.getElementById('newNumDesks').value;
    const existingRoom = document.getElementById('existingRooms').value;
    
    if (!newRoomName && !existingRoom) {
        alert('Please select an existing room or enter a new room name.');
        return;
    }

    if (newRoomName && !newNumDesks) {
        alert('Please select the number of desks for the new room.');
        return;
    }
    
    const desksForm = document.getElementById('desksForm');
    const desksContainer = document.getElementById('desksContainer');
    
    // Clear any existing desks
    desksContainer.innerHTML = '';

    let numDesks = 0;
    let roomName = '';
    
    if (newRoomName) {
        roomName = newRoomName;
        numDesks = newNumDesks;
        
        // Save the new room details
        rooms.push({ name: roomName, desks: [] });
        populateRoomOptions();
    } else {
        roomName = existingRoom;
        const room = rooms.find(r => r.name === roomName);
        numDesks = room.desks.length;
    }

    for (let i = 1; i <= numDesks; i++) {
        addDesk();
    }
    
    // Hide room selection form and show desks form
    document.getElementById('roomSelectionForm').style.display = 'none';
    desksForm.style.display = 'block';
}

function addDesk() {
    const desksContainer = document.getElementById('desksContainer');
    const deskNumber = desksContainer.children.length + 1;
    
    const deskDiv = document.createElement('div');
    deskDiv.classList.add('desk');
    
    const deskLabel = document.createElement('label');
    deskLabel.textContent = `Desk ${deskNumber}`;
    deskDiv.appendChild(deskLabel);
    
    const deskSelect = document.createElement('select');
    deskSelect.name = `desk${deskNumber}Status`;
    deskSelect.required = true;
    
    const optionAvailable = document.createElement('option');
    optionAvailable.value = 'available';
    optionAvailable.textContent = 'Available';
    
    const optionBooked = document.createElement('option');
    optionBooked.value = 'booked';
    optionBooked.textContent = 'Booked';
    
    deskSelect.appendChild(optionAvailable);
    deskSelect.appendChild(optionBooked);
    
    deskDiv.appendChild(deskSelect);
    
    const timingsDiv = document.createElement('div');
    timingsDiv.classList.add('timings');
    
    const timing1 = document.createElement('div');
    timing1.innerHTML = `<input type="checkbox" name="desk${deskNumber}Timing1" value="8 AM - 4 PM"><label>8 AM - 4 PM</label>`;
    
    const timing2 = document.createElement('div');
    timing2.innerHTML = `<input type="checkbox" name="desk${deskNumber}Timing2" value="4 PM - 12 AM"><label>4 PM - 12 AM</label>`;
    
    const timing3 = document.createElement('div');
    timing3.innerHTML = `<input type="checkbox" name="desk${deskNumber}Timing3" value="12 AM - 8 AM"><label>12 AM - 8 AM</label>`;
    
    timingsDiv.appendChild(timing1);
    timingsDiv.appendChild(timing2);
    timingsDiv.appendChild(timing3);
    
    deskDiv.appendChild(timingsDiv);
    
    desksContainer.appendChild(deskDiv);
}

function loadRoomDetails() {
    const roomName = document.getElementById('existingRooms').value;
    if (!roomName) return;
    
    const room = rooms.find(r => r.name === roomName);
    
    const desksContainer = document.getElementById('desksContainer');
    desksContainer.innerHTML = '';
    
    room.desks.forEach((desk, index) => {
        addDesk();
        const deskDiv = desksContainer.children[index];
        deskDiv.querySelector('select').value = desk.status;
        
        desk.timings.forEach(timing => {
            deskDiv.querySelector(`input[value="${timing}"]`).checked = true;
        });
    });

    // Hide room selection form and show desks form
    document.getElementById('roomSelectionForm').style.display = 'none';
    document.getElementById('desksForm').style.display = 'block';
}

function populateRoomOptions() {
    const existingRoomsSelect = document.getElementById('existingRooms');
    existingRoomsSelect.innerHTML = '<option value="" disabled selected>Select a room</option>';
    
    rooms.forEach(room => {
        const option = document.createElement('option');
        option.value = room.name;
        option.textContent = room.name;
        existingRoomsSelect.appendChild(option);
    });
}

document.getElementById('finalForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const roomName = document.getElementById('newRoomName').value || document.getElementById('existingRooms').value;
    const room = rooms.find(r => r.name === roomName);
    const desksContainer = document.getElementById('desksContainer');
    
    room.desks = Array.from(desksContainer.children).map((deskDiv, index) => {
        const status = deskDiv.querySelector('select').value;
        const timings = Array.from(deskDiv.querySelectorAll('input[type="checkbox"]:checked')).map(input => input.value);
        
        return { number: index + 1, status, timings };
    });
    
    alert('Form submitted!');
});


const togglePassword = document.querySelector('#togglePassword');
        const password = document.querySelector('#password');

        togglePassword.addEventListener('click', function () {
            const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
            password.setAttribute('type', type);

            this.classList.toggle('fas fa-eye');
        });