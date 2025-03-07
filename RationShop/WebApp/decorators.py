from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def check_approval(user):
    if user.is_authenticated and hasattr(user, 'beneficiary_profile'):
        return user.beneficiary_profile.is_approved
    return True  # Allow shop owners/admins

def approval_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not check_approval(request.user):
            return redirect('pending_approval')  # Redirect to a waiting page
        return view_func(request, *args, **kwargs)
    return _wrapped_view
