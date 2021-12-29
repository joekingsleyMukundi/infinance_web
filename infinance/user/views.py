
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import Dashboard, Cards, Reminder, Transactions
import random
from datetime import date


def registerUser(request):
    if request.user.is_authenticated:
        return redirect('userDashboard')
    formItems = CustomUserCreationForm()
    context = {'form': formItems}
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome ' + request.user.get_username())
            return redirect('userDashboard')
        else:
            messages.error(
                request, 'an error occrured during registration please contact customer care')
            return render(request, 'user/auth-register-basic.html', context)

    else:
        return render(request, 'user/auth-register-basic.html', context)


@login_required(login_url='userLogin')
def emailVerification(request):
    userOtp = request.user.dashboard.otp
    userEmail = request.user.email
    is_verified = request.user.dashboard.is_verified
    context = {'useremail': userEmail}
    if is_verified == 0:
        if request.method == 'POST':
            otpEntered = request.POST['otp']
            if str(userOtp) == otpEntered:
                try:
                    userdashboard = request.user.dashboard
                    userdashboard_id = userdashboard.id
                    userDashboardDetails = Dashboard.objects.get(
                        id=userdashboard_id)
                    userDashboardDetails.is_verified = True
                    userDashboardDetails.save()
                    return redirect('userDashboard')
                except:
                    messages.error(
                        request, 'Something went wrong contact  customer service')
                    return redirect('emailVrification')
            else:
                messages.error(
                    request, 'You Entered the wrong Verification code')
                return redirect('emailVrification')
        else:
            return render(request, 'user/auth-verify-email-cover.html', context)
    else:
        return redirect('userDashboard')


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('userDashboard')

    if request.method == 'POST':
        user_email = request.POST['login-email']
        user_password = request.POST['login-password']
        try:
            user = User.objects.get(email=user_email)
        except:
            messages.error(request, 'User doesnot exist.')
            return render(request, 'user/auth-login-basic.html')
        user = authenticate(request, email=user_email, password=user_password)
        if user is not None:
            login(request, user)
            return redirect('userDashboard')
        else:
            messages.error(request, 'username or password is incorrect')
            return render(request, 'user/auth-login-basic.html')
    else:
        return render(request, 'user/auth-login-basic.html')


@login_required(login_url='userLogin')
def dashboardUser(request):
    if request.user.dashboard.is_verified == 0:
        return redirect('emailVrification')
    else:
        user_dashboard_data = request.user.dashboard
        user_profit_made = 0
        if request.user.dashboard.monthly_capital == '0':
            user_profit_made = 0
        else:
            user_monthly_capital = request.user.dashboard.monthly_capital
            user_balance = request.user.dashboard.balance
            user_profit_made = (
                (int(user_balance)-int(user_monthly_capital))/int(user_monthly_capital))*100
            user_transactions = None
            user_cards = None
        try:
            user_transactions = user_dashboard_data.transactions_set.all()
        except:
            user_transactions = None
        try:
            user_cards = request.user.dashboard.cards_set.all()
        except:
            user_cards = None

        user_total_transactions = 0
        user_total_payouts = 0
        if user_transactions != None:
            if len(user_transactions) != 0:
                user_total_transactions = len(user_transactions)
                for user_transaction in user_transactions:
                    if user_transaction.type == 'payout':
                        user_total_payouts = user_total_payouts + user_transaction.amount
            else:
                user_total_transactions = 0
                user_total_payouts = 0
        user_total_cards = 0
        user_savings = 0
        if user_cards != None:
            if len(user_cards) != 0:
                user_total_cards = len(user_cards)
                for user_card in user_cards:
                    if user_card.title == 'savings':
                        user_savings = user_card.balance
        context = {
            'user_data': request.user,
            'user_dashboard': user_dashboard_data,
            'user_transactions': user_total_transactions,
            'user_payouts': user_total_payouts,
            'profits': user_profit_made,
            'cards': user_total_cards,
            'savings': user_savings,
            'user_total_cards': user_cards,
            'user_total_transactions': user_transactions
        }
        return render(request, 'user/index.html', context)


@login_required(login_url='userLogin')
def remindersUser(request):
    user_dashboard_data = request.user.dashboard
    if request.method == 'POST':
        title = request.POST['title']
        due_date = request.POST['due_date']
        amount = request.POST['amount']
        tags = request.POST['tags']
        card = request.POST['card']
        payment_mode = request.POST['payment']
        if title is None or due_date is None or amount is None or tags is None or card is None or payment_mode is None:
            messages.error(request, 'you cannot have empty values')
            return redirect('reminders')
        else:
            try:
                card_instance = Cards.objects.get(id=card)
                dashboard_instance = request.user.dashboard
                reminder = Reminder(name=title, dashboard=dashboard_instance,  balance=amount, due_date=due_date,
                                    card=card_instance, tags=tags, is_autopay=payment_mode)
                reminder.save()
                messages.success(request, 'successfully added')
                return redirect('reminders')
            except Exception as e:
                print(e)
                messages.error(request, 'error occured contact support')
                return redirect('reminders')
    else:
        user_reminders = user_dashboard_data.reminder_set.all()
        user_cards = request.user.dashboard.cards_set.all()
        user_total_cards = len(user_cards)
        user_reminders_length = len(user_reminders)
        context = {
            'user_data': request.user,
            'user_dashboard': user_dashboard_data,
            'user_reminders': user_reminders,
            'user_reminders_length': user_reminders_length,
            'user_cards': user_cards,
            'user_cards_length': user_total_cards
        }
        return render(request, 'user/reminders.html', context)


@login_required(login_url='userLogin')
def deleteReminder(request, pk):
    if pk is None:
        messages.error(
            request, 'error cant find your reminder')
        return redirect('reminders')
    user_dashboard_data = request.user.dashboard
    try:
        reminder_info = user_dashboard_data.reminder_set.get(id=pk)
        message = None
        if reminder_info.is_deleted == 0:
            reminder_info.soft_delete()
            message = 'You have succefully deleted the reminder'
        else:
            reminder_info.restore()
            message = 'You have succefully restored the reminder'
        messages.success(request, message)
        return redirect('reminders')
    except:
        messages.error(
            request, 'something went wrong check if you have selected the right reminder or contact support')
        return redirect('reminders')


@login_required(login_url='userLogin')
def transactionsUser(request):
    user_dashboard_data = request.user.dashboard
    user_transactions = None
    try:
        user_transactions = user_dashboard_data.transactions_set.all()
    except Exception as e:
        print(e)
        messages.error(request, 'Something went wrong contact support')
        return redirect('transaction')
    user_total_transactions = len(user_transactions)
    context = {
        'total_transactions': user_total_transactions,
        'transactions': user_transactions,
        'user_data': request.user,
        'user_dashboard': user_dashboard_data,
    }
    return render(request, 'user/transactions.html', context)


@login_required(login_url='userLogin')
def deletetransaction(request, pk):
    if pk is None:
        messages.error(
            request, 'error cant find your transaction')
        return redirect('transaction')
    user_dashboard_data = request.user.dashboard
    try:
        transaction_info = user_dashboard_data.transactions_set.get(id=pk)
        message = None
        if transaction_info.is_deleted == 0:
            transaction_info.soft_delete()
            message = 'You have succefully deleted the transaction'
        else:
            transaction_info.restore()
            message = 'You have succefully restored the transaction'
        messages.success(
            request, message)
        return redirect('transaction')
    except Exception as e:
        print(e)
        messages.error(
            request, 'something went wrong  contact support')
        return redirect('transaction')


@login_required(login_url='userLogin')
def usercards(request):
    user_dashboard_data = request.user.dashboard
    user_cards = request.user.dashboard.cards_set.all()
    user_total_cards = len(user_cards)
    if request.method != 'POST':
        context = {
            'user_data': request.user,
            'user_dashboard': user_dashboard_data,
            'total_cards': user_total_cards,
            'cards': user_cards,
        }
        return render(request, 'user/cards.html', context)
    card_title = request.POST['title']
    initial_deposite = request.POST['initdeposite']
    if card_title is None and initial_deposite is None:
        messages.error(request, 'you cannot have empty values')
        return redirect('usercards')
    user_wallet_balance = int(request.user.dashboard.balance)
    if user_wallet_balance < int(initial_deposite):
        messages.error(
            request, 'you dont have enough balance to make that transaction')
        return redirect('usercards')
    try:
        card_number_semi = random.randint(100000000000, 999999999999)
        today = date.today()
        exp_date = today.replace(year=today.year + 3)
        card_number = '5570'+str(card_number_semi)
        user_new_card = Cards(title=card_title, card_number=card_number, dashboard=user_dashboard_data,
                              balance=initial_deposite, revenue='0', spent='0', expires_at=exp_date)
        user_new_card.save()
        messages.success(request, 'you have created a new card')
        return redirect('usercards')
    except Exception as e:
        print(e)
        messages.error(request, 'error in creating new card contact support')
        return redirect('usercards')


@login_required(login_url='userLogin')
def deletecard(request, pk):
    if pk is None:
        messages.error(
            request, 'error cant find your card')
        return redirect('usercards')
    user_dashboard_data = request.user.dashboard
    try:
        card_info = user_dashboard_data.catd_set.get(id=pk)
        message = None
        if card_info.is_deleted == 0:
            card_info.soft_delete()
            message = 'You have succefully deleted the card'
        else:
            card_info.restore()
            message = 'You have succefully restored the card'
        messages.success(
            request, message)
        return redirect('usercards')
    except Exception as e:
        print(e)
        messages.error(
            request, 'something went wrong  contact support')
        return redirect('usercards')


@login_required(login_url='userLogin')
def depositeUser(request):
    return render(request, 'user/deposite.html')


@login_required(login_url='userLogin')
def withdrawUser(request):
    return render(request, 'user/withdrow.html')


@login_required(login_url='userLogin')
def sendMoneyUser(request):
    return render(request, 'user/sendmoney.html')


def logoutUser(request):
    logout(request)
    return redirect('userLogin')
# Create your views here.
