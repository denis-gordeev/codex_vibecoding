<template>
  <div>
    <h1>Nendoroid Viewer</h1>
    <div>
      <label>Fandom:
        <input v-model="filters.fandom" />
      </label>
      <label>Season:
        <input v-model="filters.season" />
      </label>
      <button @click="load">Load</button>
    </div>
    <ul>
      <li v-for="fig in figures" :key="fig.id">
        <h3>{{ fig.name }}</h3>
        <p>{{ fig.description }}</p>
        <small>Announced: {{ fig.announcement_date }} | Release: {{ fig.release_date }}</small>
        <div class="images">
          <img v-for="(img, idx) in fig.images" :key="idx" :src="img" alt="" />
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const figures = ref([])
const filters = ref({ fandom: '', season: '' })

async function load() {
  const params = {}
  if (filters.value.fandom) params.fandom = filters.value.fandom
  if (filters.value.season) params.season = filters.value.season
  const { data } = await axios.get('/api/nendoroids', { params })
  figures.value = data
}
</script>
