<script setup>
const { data: products } = await useFetch("http://localhost:8000/products")
</script>

<template>
  <div class="container">
    <h1>Product List</h1>

    <NuxtLink to="/create" class="link">Add New Product</NuxtLink>

    <ul>
      <li v-for="product in products" :key="product.id" class="product-item">
        <strong>{{ product.title }}</strong>: {{ product.description }}
      </li>
    </ul>
  </div>
</template>

<style scoped>
.container {
  max-width: 600px;
  margin: 50px auto;
}

.link {
  display: inline-block;
  margin-bottom: 20px;
  color: blue;
}

.product-item {
  background: #f0f0f8;
  padding: 12px 16px;
  margin: 8px 0;
  border-radius: 6px;
  list-style: none;
}
</style>