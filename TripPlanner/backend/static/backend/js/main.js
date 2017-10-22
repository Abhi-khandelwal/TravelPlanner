(function() {
	var destinationCount = 1;
	document.getElementById("addDestination").addEventListener("click", function(){
	    document.getElementById("destination-container").innerHTML += `<div class="form-group">
          <div class="row">
            <div class="col-4">
              <label for="destination-1">Destination 1:</label>
            </div>
            <div class="col-4">
              <input type="text" class="form-control" id="destination-1" name="destination-1">
            </div>
            <div class="col-2">
              <input type="number" class="form-control" id="destination-duration-1" name="destination-duration-1" placeholder="DUR">
            </div>
            <div class="col-2">
              <button class="btn btn-outline-danger">Delete</button>
            </div>
          </div>
        </div>`;
	    destinationCount++;
	});
})();