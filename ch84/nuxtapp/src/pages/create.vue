<script setup>
import { ref } from "vue"

const title = ref("")
const description = ref("")
const router = useRouter()

const handleSubmit = async () => {
  try {
    const res = await fetch(
      "http://localhost:8000/products",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          title: title.value,
          description: description.value
        })
      }
    )

    if (res.ok) {
      router.push("/")
    } else {
      alert("Error creating product")
    }
  } catch (err) {
    console.error(err)
    alert("Server error")
  }
}
</script>

<template>
  <div class="container">
    <h1>Add Product</h1>

    <form @submit.prevent="handleSubmit">
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
        Add
      </button>
    </form>

    <NuxtLink
      to="/"
      class="link"
    >
      Back to List
    </NuxtLink>
  </div>
</template>

<style scoped>
.container {
  max-width: 600px;
  margin: 50px auto;
  text-align: center;
}

input,
textarea {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
}

button {
  padding: 10px 20px;
  cursor: pointer;
}

.link {
  display: block;
  margin-top: 20px;
}
</style>