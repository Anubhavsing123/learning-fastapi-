import {useState} from 'react'

const ProductForm = ({onProductAdd}) => {
    const [title,settitle]=useState('');
    const [description,setdescription]=useState('');
    const handleSubmit=async (e)=>{
        e.preventDefault();
        const res=await fetch('http://localhost:8000/products',{
            method:"POST",
            headers:{
                "Content-Type":'application/json',
            },
            body:JSON.stringify({title,description})
        });
        if (res.ok){
            settitle('');
            setdescription('')
            const newProduct=await res.json();
            onProductAdd(newProduct);
        }
        else{
            alert("error")
        }
    }
  return (
    <form onSubmit={handleSubmit}>
        <h2>ADD product</h2>
        <input
        type="text"
        placeholder="title"
        value={title}
        onChange={(e)=>settitle(e.target.value)}
        required
        />
        <br/>
       <textarea
  placeholder="description"
  value={description}
  onChange={(e) => setdescription(e.target.value)}
  required
></textarea>
        <br/>
        <button type="submit">ADD</button>
    </form>
  )
}

export default ProductForm