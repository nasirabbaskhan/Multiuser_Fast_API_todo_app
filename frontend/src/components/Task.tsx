"use client"
import {  Edit, Trash, Trash2 } from 'lucide-react'
import React from 'react'

import { CiSquareCheck } from 'react-icons/ci'
import { Todo } from '@/lib/type'
import ToolTip from './ToolTip'
import { EditTask } from './EditTask'
import { delete_todo } from '@/action/action'
import toast from 'react-hot-toast'
type Props={
    id:number
    content:string
    is_completed:boolean
}

export default function Task(task:Props) {
  const handleDelete= async (id:number)=>{
    console.log("delete")
    const respnse= await delete_todo(id)
    const{status,message}= respnse
    if(status=='success'){
     toast.success(message)
    }else{
      toast.error(message)
    }
  }
  return (
    <>
    <div className=' flex justify-between py-1 px-3 my-2 '>
          <p >{task.content}</p>
          <div className='flex items-center gap-2'>
            <div className="check">
            <ToolTip too_tip_content='Mark as competed'>
            <CiSquareCheck size={23} className={`cursor-pointer ${task.is_completed?"text-green-900":"text-gray-300"} `}/>
            </ToolTip>
            </div>
            
            <div className="edit">
            <ToolTip too_tip_content='Edit Task'>
            {/* <Edit className='text-blue-300 cursor-pointer' size={19}/> */}
            <EditTask id={task.id} content={task.content} is_completed={task.is_completed}/>
            </ToolTip>
            </div>
            
            <div className="delete">
            <ToolTip too_tip_content='Delete Task'>
              {/* <DeleteTask/> */}
              <Trash2 onClick={()=>handleDelete(task.id)}  className='text-red-600 cursor-pointer' size={21}/>
              </ToolTip>
              
          
            </div>
           
          </div>
         
        </div> 
        <div className="line bg-gray-500 w-full h-0.5"></div>
        </>
  )
}
