import React from 'react'
import Task from './Task'
import { Todo } from '@/lib/type'
import { get_todo } from '@/action/action'

export default async function TaksTable() {
  const todo_list:Todo[]= await get_todo()
  // const response= await fetch("http://127.0.0.1:8080/todos/")
  // const todo_lost:Todo[]= await response.json()

    // const todo_lost:Todo[]=[
    //     {id:1, content:"First Task", is_completed:false},
    //     {id:2, content:"Second Task", is_completed:false},
    //     {id:3, content:"Third Task", is_completed:false},
    //     {id:4, content:"Fourth Task", is_completed:false},
    //     {id:5, content:"Fifth Task", is_completed:false},
    //     {id:6, content:"sixth Task", is_completed:true},
    // ]
  return (
    <section className='main w-full border rounded border-black px-2 '>
        <div className='bg-gray-300 flex justify-between py-1 px-3 my-2 rounded shadow-md'>
          <p className='text-lg'>TASKS</p>
          <p className='text-lg'>ACTIONS</p>
        </div>
       <div className="task">
          {todo_list.map((item,index)=>{
            return(
           <Task key={index} content={item.content} id={item.id} is_completed={item.is_completed}/>
        
            )
          }
          )}  
        
    
        </div> 

    </section>
  )
}
