import Image from "next/image"

export default function Header() {
  return (
    <section className=' py-2 px-2 flex gap-4 ml-10'>
        <div className="logo">
        <Image src={"/logo1.jpg"} height={50} width={70} alt="logo"/>
        </div>
        <div className="todo">
            <h1 className='text-3xl font-bold  '>TODO</h1>
            <p className='text-gray-500'>Tick, Tack, todo&apos;s on track- Organize, Prioritize and Relax!</p>
        </div>
      
    </section>
  )
}
