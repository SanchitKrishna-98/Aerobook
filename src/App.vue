<template>
    <!-- Title and Icons -->
    <div class="row">

      <div class="container-fluid bg-info py-3">
        <div class="col-md-12 text-center">
  <!-- Title -->
  <h1 class="text-lighter mb-0"><i class="fas fa-plane"></i> AeroBook: Where Your Dreams Take Flight!!!</h1>
</div>
    </div>
    </div>

    <!-- Search Form -->
    <div class="row mt-4">
  <div class="col-md-6">
    <div class="form-group">
      <label for="originInput" class="text-light">Origin City</label>
      <input v-model="origin" id="originInput" class="form-control" placeholder="Enter origin city ID">
    </div>
  </div>
  <div class="col-md-6">
    <div class="form-group">
      <label for="destinationInput" class="text-light">Destination City</label>
      <input v-model="destination" id="destinationInput" class="form-control" placeholder="Enter destination city ID">
    </div>
  </div>
</div>
<div class="col-md-12 text-center">
  <div class="form-group">
    <label>&nbsp;</label><br>
    <button @click="searchFlights" class="btn btn-primary">Submit</button>
  </div>
</div>


    <!-- Flight Results -->
    <div class="row mt-12 text-center">
      <div class="col-md-12 text-center">
        <label>&nbsp;</label><br>
        <div v-if="flights.length === 0" class="alert alert-info" role="alert">
          No flights found.
        </div>
        <div v-else>
          <div v-for="flight in flights" :key="flight.flight_id" class="card mb-3">
            <div class="card-body">
              <h5 class="card-title">Flight Details</h5>
              <p class="card-text">Airline Name: {{ flight.airline_name}}</p>
              <p class="card-text">Departure Time: {{ flight.departure_time }}</p>
              <p class="card-text">Arrival Time: {{ flight.arrival_time }}</p>
              <p class="card-text">Flight Status: {{ flight.flight_status }}</p>
              <p class="card-text">Flight ID: {{ flight.flight_id }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      origin: '',
      destination: '',
      flights: []
    };
  },
  methods: {
    searchFlights() {
      const body = {
        origin: this.origin,
        destination: this.destination
      };
      axios.post('http://127.0.0.1:5000/search_flights', body)
      .then(response => {
        this.flights = response.data;
        console.log(this.flights);
      })
      .catch(error => console.error('Error:', error));
    }
  }
}
</script>

<style scoped></style>
