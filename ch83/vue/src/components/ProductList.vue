<script setup>
import { ref, onMounted } from 'vue'
import ProductForm from './ProductForm.vue'

const products = ref([])

const fetchProducts = async () => {
  try {
    const res = await fetch('http://localhost:8000/products')

    if (res.ok) {
      products.value = await res.json()
    }
  } catch (error) {
    console.error(error)
  }
}

const addProduct = (newProduct) => {
  products.value.push(newProduct)
}

onMounted(fetchProducts)
</script>

<template>
  <div>
    <ProductForm @product-add="addProduct" />

    <hr />

    <h2>Product List</h2>

    <ul>
      <li
        v-for="product in products"
        :key="product.id"
      >
        <strong>{{ product.title }}</strong>
        <p>{{ product.description }}</p>
      </li>
    </ul>
  </div>
</template>

<style scoped>
div {
  max-width: 800px;
  margin: auto;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  background: #f5f5f5;
  margin-bottom: 10px;
  padding: 15px;
  border-radius: 8px;
}

strong {
  color: #42b883;
}
</style>