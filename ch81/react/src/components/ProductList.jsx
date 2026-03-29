import {useEffect,useState} from 'react';
import ProductForm from "./ProductForm"

const ProductList = () => {
    const [products,setProduct]=useState([]);
    const fecthProducts=async ()=>{
        const res=await fetch("http://localhost:8000/products");
        const data=  await res.json();
        setProduct(data)

    };
    useEffect(()=>{
        fecthProducts()
    },[])
  return (
    <div>
        <ProductForm onProductAdd={(product)=>setProduct([...products,product])}></ProductForm>
        <hr/>
        <ul>
            {products.map((p)=>
            <li key={p.id}
            >
                <strong>{p.title}</strong>:{p.description}
            </li>
            )}
        </ul>
    </div>
  )
}

export default ProductList