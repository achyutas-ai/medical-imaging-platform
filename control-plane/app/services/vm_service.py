from typing import List, Optional
import uuid
# import paramiko  # To be used later

from app.schemas.vm import VM, VMCreate, VMUpdate

class VMService:
    def __init__(self):
        # Placeholder for VM storage
        self._vms = {}

    def create_vm(self, vm_in: VMCreate) -> VM:
        vm_id = str(uuid.uuid4())
        vm = VM(
            id=vm_id,
            status="provisioning",
            ip_address="192.168.1.100", # Placeholder
            **vm_in.model_dump()
        )
        self._vms[vm_id] = vm
        return vm

    def get_vm(self, vm_id: str) -> Optional[VM]:
        return self._vms.get(vm_id)

    def list_vms(self) -> List[VM]:
        return list(self._vms.values())

    def update_vm(self, vm_id: str, vm_in: VMUpdate) -> Optional[VM]:
        if vm_id not in self._vms:
            return None
        
        vm = self._vms[vm_id]
        update_data = vm_in.model_dump(exclude_unset=True)
        
        # Create a new VM object with updated data
        updated_vm = vm.model_copy(update=update_data)
        self._vms[vm_id] = updated_vm
        return updated_vm

    def delete_vm(self, vm_id: str) -> bool:
        if vm_id in self._vms:
            del self._vms[vm_id]
            return True
        return False

vm_service = VMService()
