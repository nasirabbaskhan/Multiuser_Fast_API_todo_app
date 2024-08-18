"use client"
import { add_todo } from "@/action/action"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { useState } from "react"
import toast from "react-hot-toast"
import * as yup from "yup";


export function AddToTask() {
  //for validation
  const taskValidationSchema = yup.object().shape({
    task: yup.string().required().max(40).min(4),
  
  });
  const [errors, setErrors] = useState([]);
const [task,setTask]= useState("")
  const [done,setDone] = useState(false)
  const handlClick=async ()=>{
    try {
      const result= await taskValidationSchema.validate({ task });
      if(!result){
        return
      }
      setErrors([]);

      setDone(true)
    const response=await add_todo(task)
    const {status,message}= response
    if(status=='success'){
    setTask("")
    setDone(false)
    toast.success(message)
    }
    else{
      toast.error(message)
    }
    
      
    } catch (err:any) {
      setErrors(err.errors)
      
    }

  }
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant={"default"} className="bg-teal-600 w-full uppercase ">Add Task +</Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Add New Task</DialogTitle>
        
        </DialogHeader>
            <Input
            onChange={(e)=>setTask(e.target.value)}
              type="text"
              placeholder="Add task here"
              minLength={3}
              maxLength={54}
              required
              value={task}
              className="w-full"
            />
              <div className="mt-7">
              
              {errors.map((item, index) => {
                return <div key={index} className="text-red-600">{item}</div>;
              })}
            </div>
          <button  onClick={handlClick}  className={`text-white w-full py-2 rounded ${task?"bg-blue-600": "bg-blue-400"} `}>{done?"Saving...":"Save"} </button>
      </DialogContent>
    </Dialog>
  )
}
