'use client'
import {useEffect,useState} from 'react'
import Link from 'next/link'

export default function Home() {
  const [product,setProduct]=useState([])
  useEffect(()=>{
    fetch('http://localhost:8000/products')
    .then((res)=>res.json())
    .then((data)=>setProduct(data))
    .catch((err)=>console.error("Error fetching products:",err))

  },[])
  return (
    <main style ={{maxWidth:'600px',margin:'40px auto',padding:'1rem'}}>
      <h1 style={{fontsize:'2rem',fontWeigth:'bold'}}>Product List</h1>
      <Link href='/create' style={{color:"blue",textDecoration:"underline"}}>ADD NEWPRODUCT</Link>
       <div style={{ marginTop: '20px' }}>
        {product.map((item) => (
          <div
            key={item.id}
            style={{
              border: '1px solid #ccc',
              padding: '10px',
              marginBottom: '10px',
              borderRadius: '6px',
            }}
          >
            <h3>{item.title}</h3>
            <p>{item.description}</p>
          </div>
        ))}
      </div>
    </main>
  );
}
