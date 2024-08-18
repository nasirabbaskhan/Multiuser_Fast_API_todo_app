import { AddToTask } from "@/components/AddTask";
import TaksTable from "@/components/TaksTable";
import Image from "next/image";

export default function Home() {
  return (
    <div className="w-[900px] mx-auto mt-10 px-7">
    {/* add the task button */}
    <section >
     <AddToTask/>
  </section>

    {/* To do Table */}
    <section className="mt-3">
    <TaksTable/>
    </section>
    
    </div>

  );
}
