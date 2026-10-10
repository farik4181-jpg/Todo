from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
def task_list(request):
    # Якщо форма відправлена, створюємо нове завдання
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Task.objects.create(title=title)
        return redirect('task_list')

    # Отримуємо всі завдання з бази
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'todo/task_list.html', {'tasks': tasks})


# ... ваша існуюча функція task_list ...
def task_list(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Task.objects.create(title=title)
        return redirect('task_list')

    # Отримуємо параметри з URL
    status = request.GET.get('status', 'all')
    search_query = request.GET.get('q', '') # Зчитуємо пошуковий запит

    # Базова вибірка всіх завдань
    tasks = Task.objects.all()

    # 1. Застосовуємо фільтр статусу
    if status == 'active':
        tasks = tasks.filter(completed=False)
    elif status == 'completed':
        tasks = tasks.filter(completed=True)

    # 2. Застосовуємо пошук, якщо є текст
    if search_query:
        # title__icontains шукає частковий збіг тексту (незалежно від регістру)
        tasks = tasks.filter(title__icontains=search_query)

    # 3. Сортуємо результат
    tasks = tasks.order_by('-created_at')

    # Передаємо змінні в шаблон
    return render(request, 'todo/task_list.html', {
        'tasks': tasks, 
        'current_status': status,
        'search_query': search_query # Передаємо запит, щоб залишити його в полі вводу
    })


# --- НОВІ ФУНКЦІЇ ---

def complete_task(request, task_id):
    # Шукаємо завдання за ID
    task = get_object_or_404(Task, id=task_id)
    # Перемикаємо статус на протилежний (якщо False, стане True і навпаки)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete() # Видаляємо з бази
    return redirect('task_list')

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        # Отримуємо новий текст з форми
        new_title = request.POST.get('title')
        if new_title:
            task.title = new_title
            task.save() # Це автоматично оновить поле updated_at
        return redirect('task_list')
        
    # Якщо це GET-запит, просто показуємо сторінку з формою
    return render(request, 'todo/edit_task.html', {'task': task})