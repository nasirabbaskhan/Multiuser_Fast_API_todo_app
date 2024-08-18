"use client"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Edit } from "lucide-react"
import { useState } from "react"
import ToolTip from "./ToolTip"
import { update_todo } from "@/action/action"
import toast, { Toaster } from "react-hot-toast"
import * as yup from "yup";

type Props={
    id:number
    content:string
    is_completed:boolean
    
}

export function EditTask(props:Props) {
  //for validation
  const taskValidationSchema = yup.object().shape({
    editTask: yup.string().required().max(40).min(4),
  
  });
  const [errors, setErrors] = useState([]);
  const [editTask,setEditTask]= useState("")
  const [selected,setSelected]= useState<string>()
  const [edited,setEdited]= useState(false)
  
  const completed = Boolean(Number(selected))
 
  const handlClick=async (id:number)=>{

    try {
      const result= await taskValidationSchema.validate({ editTask });
      if(!result){
        return
      }
      setErrors([]);

      setEdited(true);

      const response = await update_todo(id, editTask,completed);
      const { status, message, err } = response;

      if (status === "success") {
        setEditTask("");
        setEdited(false);
        toast.success(message);
      } else {
        toast.error(message);
        
      }
    } catch (err:any) {
      setErrors(err.errors);
     
    }
   
    
  }
  return (
    <Dialog>
      <DialogTrigger asChild>
      
      <Edit className='text-blue-300 cursor-pointer' size={19}/> 
      
        </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Edit Task</DialogTitle>
        
        </DialogHeader>
          <div className="flex justify-between">
            <p>Task ID: {props.id}</p>
           <div>
           <label htmlFor="todo">Completed:</label>
            <select onChange={(e)=>{setSelected(e.target.value)}} id="todo">
               
               <option value={0 } >False</option>
               <option value={1} >True</option>
               
            </select>
           </div>
          </div>
            <Input
            onChange={(e)=>setEditTask(e.target.value)}
              type="text"
              placeholder="Write here..."
              minLength={3}
              maxLength={54}
              required
              value={editTask}
              className="w-full"
            />
           
            
            <div className="mt-7">
              
            {errors.map((item, index) => {
              return <div key={index} className="text-red-600">{item}</div>;
            })}
          </div>
           
          <button  onClick={()=>handlClick(props.id)}  className={`text-white w-full py-2 rounded ${editTask?"bg-blue-600": "bg-blue-400"} `}>{edited?"Saving...":"Edit"}
           
         </button>
      </DialogContent>
    </Dialog>
  )
}
