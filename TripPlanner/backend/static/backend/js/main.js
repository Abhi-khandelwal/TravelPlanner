(function() {
	var destinationCount = 1;
	document.getElementById("addDestination").addEventListener("click", function(){
	    document.getElementById("destination-container").innerHTML += `<div class="form-group" id="destination-`+ destinationCount+`">
          <div class="row">
            <div class="col-4">
              <label for="destination-1">Destination `+ destinationCount +`:</label>
            </div>
            <div class="col-4">
              <input type="text" class="form-control" id="destination-name-` + destinationCount + `" name="destination-` + destinationCount + `">
            </div>
            <div class="col-2">
              <input type="number" class="form-control" id="destination-duration-` + destinationCount + `" name="destination-duration- ` + destinationCount + `" placeholder="DUR">
            </div>
            <div class="col-2">
              <button class="btn btn-outline-danger">Delete</button>
            </div>
          </div>
        </div>`;
	    destinationCount++;
	    document.getElementById("removeDestination-" + destinationCount).addEventListener("click", function(){
	    	document.getElementById("destination"+ destinationCount).remove();
		});
	});
})();