import { UserCircle } from 'lucide-react'
import Image from 'next/image'
import React from 'react'

const WorkspaceHeader = () => {
  return (
    <div className='p-4 flex justify-between shadow-md'>
        <Image src={'/logo.svg'} alt='logo' width={180} height={140} />
        <UserCircle className='w-10 h-14'/>
    </div>
  )
}

export default WorkspaceHeader