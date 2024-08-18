import { Button } from "@/components/ui/button"
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"

export default function ToolTip({too_tip_content , children}:{too_tip_content:string, children:React.ReactNode}) {
  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          {children}
        </TooltipTrigger>
        <TooltipContent>
          <p>{too_tip_content}</p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  )
}
