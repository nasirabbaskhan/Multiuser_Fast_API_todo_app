"use server"

import { revalidatePath } from "next/cache"

export async function get_todo(){
    try {
        const response= await fetch("http://127.0.0.1:8000/todos/",{
            next:{
                 tags:["task"]
            },
            cache: "no-store",
        })
        const data = await response.json()
        return data
    } catch (error) {
        return {status:"error", message:"something went wronge"}

        
    }

}

export async function add_todo(task:string){
    try {
        const response= await fetch("http://127.0.0.1:8000/todos/",{
            method:"Post",
            headers:{
                'content-Type':'application/json',
            },
            body:JSON.stringify({content:task})
        })
        revalidatePath("task")
        console.log("add todo successfully")
        return {status:"success", message:"Todo addedd Successfully"}
    } catch (error) {
        return {status:"error", message:"something went wronge"}

        
    }

}


export async function delete_todo(id:number){
try {
    const response= await fetch(`http://127.0.0.1:8000/todos/${id}`,{
        method:"Delete",
        headers:{
            'content-Type':'application/json',
        },
        body:JSON.stringify({id:id})
    })
    revalidatePath("task")
    
    console.log(" task deleted successfully")
    return {status:"success", message:"Todo deleted Successfully"}
} catch (error) {
    return {status:"error", message:"something went wronge"}

    
}

}


export async function update_todo(id:number, content:string,selected:boolean){
    try {
        const response= await fetch(`http://127.0.0.1:8000/todos/${id}`,{
            method:"PUT",
            headers:{
                'content-Type':'application/json',
            },
            body:JSON.stringify({id:id,content:content,is_completed:selected})
        }
        
        )
        revalidatePath("task")
        console.log(" task updated successfully")
        return {status:"success", message:"Todo Updated Successfully"}
    } catch (err:any) {
      
        return {status:"error", message:"something went wronge", err:err}
    
        
    }
    
    }