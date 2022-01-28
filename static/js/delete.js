// delete reservation with an AJAX post request
const deleteButtons = document.querySelectorAll('.delete');

for (let button of deleteButtons) {
    button.addEventListener('submit', (evt) => {
        evt.preventDefault();

        const formData = {
            'startTime': document.querySelector(`[name="start_time_${evt.target.id}"`).value
        };

        // remove the HTML element
        document.getElementById(`row${evt.target.id}`).remove();

        // remove the reservation from the database
        fetch('/reservations/delete', {
            method: 'POST',
            body: JSON.stringify(formData),
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(res => {
            if (res.ok) {
                alert('Attempt to cancel reservation failed. Please try again');
            }
        })
    })
}
