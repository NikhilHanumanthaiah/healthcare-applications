'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getBills, createBill, getPatients, getMedicines } from '@/lib/api';
import { Bill, BillItem } from '@/types';
import { Button } from '@/components/ui/button';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Plus, FileText, Trash2 } from 'lucide-react';
import { useState } from 'react';
import { toast } from 'sonner';

export default function BillsPage() {
  const queryClient = useQueryClient();
  const [isOpen, setIsOpen] = useState(false);
  const [selectedPatientId, setSelectedPatientId] = useState<string>('');
  const [billItems, setBillItems] = useState<BillItem[]>([]);

  // Fetch data for dropdowns
  const { data: bills, isLoading: isLoadingBills, error: errorBills } = useQuery({
    queryKey: ['bills'],
    queryFn: getBills,
  });

  const { data: patients } = useQuery({
    queryKey: ['patients'],
    queryFn: getPatients,
  });

  const { data: medicines } = useQuery({
    queryKey: ['medicines'],
    queryFn: getMedicines,
  });

  const createMutation = useMutation({
    mutationFn: createBill,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['bills'] });
      setIsOpen(false);
      toast.success('Bill created successfully');
      setBillItems([]);
      setSelectedPatientId('');
    },
    onError: (err) => {
      toast.error('Failed to create bill: ' + err.message);
    },
  });

  const handleAddItem = () => {
    setBillItems([...billItems, { medicine_id: 0, quantity: 1 }]);
  };

  const handleRemoveItem = (index: number) => {
    const newItems = [...billItems];
    newItems.splice(index, 1);
    setBillItems(newItems);
  };

  const updateItem = (index: number, field: keyof BillItem, value: number) => {
    const newItems = [...billItems];
    newItems[index] = { ...newItems[index], [field]: value };
    setBillItems(newItems);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const patient = patients?.find(p => p.id?.toString() === selectedPatientId);
    if (!patient) {
      toast.error('Please select a patient');
      return;
    }

    if (billItems.length === 0) {
      toast.error('Please add at least one medicine');
      return;
    }

    // Validate items
    for (const item of billItems) {
      if (!item.medicine_id || item.medicine_id === 0) {
        toast.error('Please select a medicine for all items');
        return;
      }
      if (!item.quantity || item.quantity <= 0) {
        toast.error('Quantity must be greater than 0');
        return;
      }
    }

    const billData: Bill = {
      patient_name: `${patient.first_name} ${patient.last_name || ''}`.trim(),
      patient_age: patient.age,
      items: billItems
    };

    createMutation.mutate(billData);
  };

  const calculateTotal = () => {
    if (!medicines || billItems.length === 0) return 0;
    return billItems.reduce((acc, item) => {
      const med = medicines.find(m => m.id === item.medicine_id);
      return acc + (med ? med.price_per_unit * item.quantity : 0);
    }, 0);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Bills</h1>
          <p className="text-muted-foreground">View and manage patient bills.</p>
        </div>
        <Dialog open={isOpen} onOpenChange={setIsOpen}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="mr-2 h-4 w-4" /> Create Bill
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[600px]">
            <DialogHeader>
              <DialogTitle>Create New Bill</DialogTitle>
              <DialogDescription>
                Select patient and add medicines to create a bill.
              </DialogDescription>
            </DialogHeader>
            <form onSubmit={handleSubmit}>
              <div className="grid gap-4 py-4">
                <div className="grid gap-2">
                  <Label htmlFor="patient">Patient</Label>
                  <Select value={selectedPatientId} onValueChange={setSelectedPatientId}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select a patient" />
                    </SelectTrigger>
                    <SelectContent>
                      {patients?.map((patient) => (
                        <SelectItem key={patient.id} value={patient.id?.toString() || ''}>
                          {patient.first_name} {patient.last_name} (ID: {patient.id})
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <Label>Medicines</Label>
                    <Button type="button" variant="outline" size="sm" onClick={handleAddItem}>
                      <Plus className="h-4 w-4 mr-2" /> Add Item
                    </Button>
                  </div>
                  
                  {billItems.map((item, index) => (
                    <div key={index} className="flex items-end gap-2 border p-3 rounded-md">
                      <div className="flex-1 space-y-2">
                        <Label className="text-xs">Medicine</Label>
                        <Select 
                          value={item.medicine_id?.toString()} 
                          onValueChange={(val) => updateItem(index, 'medicine_id', parseInt(val))}
                        >
                          <SelectTrigger>
                            <SelectValue placeholder="Select medicine" />
                          </SelectTrigger>
                          <SelectContent>
                            {medicines?.map((med) => (
                              <SelectItem key={med.id} value={med.id?.toString() || ''}>
                                {med.name} (₹{med.price_per_unit})
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="w-24 space-y-2">
                        <Label className="text-xs">Qty</Label>
                        <Input 
                          type="number" 
                          min="1"
                          value={item.quantity}
                          onChange={(e) => updateItem(index, 'quantity', parseInt(e.target.value))}
                        />
                      </div>
                      <Button 
                        type="button" 
                        variant="ghost" 
                        size="icon"
                        className="text-red-500"
                        onClick={() => handleRemoveItem(index)}
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  ))}
                  
                  {billItems.length > 0 && (
                    <div className="flex justify-end font-bold">
                      Total: ₹{calculateTotal().toFixed(2)}
                    </div>
                  )}
                </div>
              </div>
              <DialogFooter>
                <Button type="submit" disabled={createMutation.isPending}>
                  {createMutation.isPending ? 'Creating...' : 'Create Bill'}
                </Button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      <div className="rounded-md border bg-card">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>ID</TableHead>
              <TableHead>Patient Name</TableHead>
              <TableHead>Age</TableHead>
              <TableHead>Total Amount</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoadingBills ? (
              <TableRow>
                <TableCell colSpan={5} className="text-center py-10">
                  Loading bills...
                </TableCell>
              </TableRow>
            ) : errorBills ? (
               <TableRow>
                <TableCell colSpan={5} className="text-center py-10 text-red-500">
                  Error loading bills.
                </TableCell>
              </TableRow>
            ) : bills?.length === 0 ? (
              <TableRow>
                <TableCell colSpan={5} className="text-center py-10">
                  No bills found.
                </TableCell>
              </TableRow>
            ) : (
              bills?.map((bill) => (
                <TableRow key={bill.id}>
                  <TableCell className="font-medium">#{bill.id}</TableCell>
                  <TableCell>{bill.patient_name}</TableCell>
                  <TableCell>{bill.patient_age}</TableCell>
                  <TableCell>₹{bill.total_amount}</TableCell>
                  <TableCell className="text-right">
                    <Button variant="ghost" size="sm">
                      <FileText className="mr-2 h-4 w-4" /> View
                    </Button>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
