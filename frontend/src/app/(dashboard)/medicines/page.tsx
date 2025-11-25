'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getMedicines, createMedicine, deleteMedicine } from '@/lib/api';
import { Medicine } from '@/types';
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
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Plus, Trash2 } from 'lucide-react';
import { useState } from 'react';
import { toast } from 'sonner';

export default function MedicinesPage() {
  const queryClient = useQueryClient();
  const [isOpen, setIsOpen] = useState(false);
  const [newMedicine, setNewMedicine] = useState<Partial<Medicine>>({
    name: '',
    price_per_unit: 0,
    stock: 0,
  });

  const { data: medicines, isLoading, error } = useQuery({
    queryKey: ['medicines'],
    queryFn: getMedicines,
  });

  const createMutation = useMutation({
    mutationFn: createMedicine,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['medicines'] });
      setIsOpen(false);
      toast.success('Medicine added successfully');
      setNewMedicine({ name: '', price_per_unit: 0, stock: 0 });
    },
    onError: (err) => {
      toast.error('Failed to add medicine: ' + err.message);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: deleteMedicine,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['medicines'] });
      toast.success('Medicine deleted successfully');
    },
    onError: (err) => {
      toast.error('Failed to delete medicine: ' + err.message);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    createMutation.mutate(newMedicine as Medicine);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Medicines</h1>
          <p className="text-muted-foreground">Manage pharmacy inventory.</p>
        </div>
        <Dialog open={isOpen} onOpenChange={setIsOpen}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="mr-2 h-4 w-4" /> Add Medicine
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[425px]">
            <DialogHeader>
              <DialogTitle>Add New Medicine</DialogTitle>
              <DialogDescription>
                Enter medicine details below.
              </DialogDescription>
            </DialogHeader>
            <form onSubmit={handleSubmit}>
              <div className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="name" className="text-right">
                    Name
                  </Label>
                  <Input
                    id="name"
                    value={newMedicine.name}
                    onChange={(e) => setNewMedicine({ ...newMedicine, name: e.target.value })}
                    className="col-span-3"
                    required
                  />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="price" className="text-right">
                    Price
                  </Label>
                  <Input
                    id="price"
                    type="number"
                    value={Number.isNaN(newMedicine.price_per_unit) ? '' : newMedicine.price_per_unit}
                    onChange={(e) => setNewMedicine({ ...newMedicine, price_per_unit: parseFloat(e.target.value) })}
                    className="col-span-3"
                    required
                  />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="stock" className="text-right">
                    Stock
                  </Label>
                  <Input
                    id="stock"
                    type="number"
                    value={Number.isNaN(newMedicine.stock) ? '' : newMedicine.stock}
                    onChange={(e) => setNewMedicine({ ...newMedicine, stock: parseInt(e.target.value) })}
                    className="col-span-3"
                    required
                  />
                </div>
              </div>
              <DialogFooter>
                <Button type="submit" disabled={createMutation.isPending}>
                  {createMutation.isPending ? 'Saving...' : 'Save changes'}
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
              <TableHead>Name</TableHead>
              <TableHead>Price</TableHead>
              <TableHead>Stock</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading ? (
              <TableRow>
                <TableCell colSpan={4} className="text-center py-10">
                  Loading medicines...
                </TableCell>
              </TableRow>
            ) : error ? (
               <TableRow>
                <TableCell colSpan={4} className="text-center py-10 text-red-500">
                  Error loading medicines.
                </TableCell>
              </TableRow>
            ) : medicines?.length === 0 ? (
              <TableRow>
                <TableCell colSpan={4} className="text-center py-10">
                  No medicines found.
                </TableCell>
              </TableRow>
            ) : (
              medicines?.map((medicine) => (
                <TableRow key={medicine.id}>
                  <TableCell className="font-medium">{medicine.name}</TableCell>
                  <TableCell>₹{medicine.price_per_unit}</TableCell>
                  <TableCell>{medicine.stock}</TableCell>
                  <TableCell className="text-right">
                    <Button 
                      variant="ghost" 
                      size="icon" 
                      className="text-red-500 hover:text-red-700"
                      onClick={() => deleteMutation.mutate(medicine.id!)}
                    >
                      <Trash2 className="h-4 w-4" />
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
