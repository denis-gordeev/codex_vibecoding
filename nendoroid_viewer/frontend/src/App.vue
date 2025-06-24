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
      <li v-for="fig in figures" :key="fig.id">{{ fig.name }} ({{ fig.release_date }})</li>
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
