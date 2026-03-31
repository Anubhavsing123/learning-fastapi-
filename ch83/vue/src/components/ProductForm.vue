<script setup>
import { ref } from 'vue'

const emit = defineEmits(['product-add'])

const title = ref('')
const description = ref('')

const submitForm = async () => {
  try {
    const res = await fetch('http://localhost:8000/products', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        title: title.value,
        description: description.value
      })
    })

    if (res.ok) {
      const data = await res.json()

      emit('product-add', data)

      title.value = ''
      description.value = ''
    } else {
      alert('Failed to add product')
    }
  } catch (error) {
    console.error(error)
  }
}
</script>

<template>
  <form @submit.prevent="submitForm">
    <h2>ADD Product</h2>

    <input
      v-model="title"
      type="text"
      placeholder="Title"
      required
    />

    <textarea
      v-model="description"
      placeholder="Description"
      required
    ></textarea>

    <button type="submit">
      ADD
    </button>
  </form>
</template>

<style scoped>
form {
  max-width: 500px;
  margin: 40px auto;
  padding: 30px;
  background: #ffffff;
  border-radius: 15px;
  box-shadow: 0 5px 20px rgba(0,0,0,0.1);
}

h2 {
  text-align: center;
  margin-bottom: 25px;
}

input,
textarea {
  width: 100%;
  padding: 12px;
  margin-bottom: 15px;
  box-sizing: border-box;
}

textarea {
  min-height: 120px;
}

button {
  width: 100%;
  padding: 12px;
  background: #42b883;
  color: white;
  border: none;
  cursor: pointer;
}
</style>