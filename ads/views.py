from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import *
from .forms import AdForm, ExchangeProposalForm
from django.db.models import Q


class AdsListView(LoginRequiredMixin, TemplateView):
    template_name = 'ads/ads.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category = self.request.GET.get('category')
        search = self.request.GET.get('search')

        ads_query = Ad.objects.all()

        if category and category != 'all':
            ads_query = ads_query.filter(category_id=category)

        if search:
            ads_query = ads_query.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(condition__icontains=search)
            )

        context['ads'] = ads_query
        context['categories'] = Categories.objects.all()

        # Здесь фильтрация по текущему пользователю
        context['proposals'] = ExchangeProposal.objects.filter(
            Q(ad_sender__user=self.request.user)
        )

        context['proposals_income'] = ExchangeProposal.objects.filter(
            Q(ad_receiver__user=self.request.user, status='wait')
        )
        return context


class AdManageView(LoginRequiredMixin, FormView):
    form_class = AdForm
    template_name = 'ads/ad_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.ad = None
        pk = kwargs.get('pk')
        if pk:
            self.ad = get_object_or_404(Ad, pk=pk, user=request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ad'] = self.ad
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.ad:
            kwargs['instance'] = self.ad
        return kwargs

    def form_valid(self, form):
        ad = form.save(commit=False)
        if not self.ad:
            ad.user = self.request.user
        ad.save()
        return JsonResponse({'status': 'ok', 'ad_id': ad.id})

    def delete(self, request, *args, **kwargs):
        if self.ad:
            self.ad.delete()
            return JsonResponse({'status': 'deleted'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Ad not found'}, status=404)


class ProposalManageView(LoginRequiredMixin, FormView):
    form_class = ExchangeProposalForm
    template_name = 'ads/change.html'

    ACTIONS = {
        'accept': ExchangeProposal.Status.ACCEPTED,
        'cancel': ExchangeProposal.Status.REJECTED,
    }

    def dispatch(self, request, *args, **kwargs):
        self.proposal = None
        pk = kwargs.get('pk')

        if pk:
            self.proposal = get_object_or_404(ExchangeProposal, pk=pk)
            self.receiver_ad = self.proposal.ad_receiver
        else:
            receiver_ad_id = request.GET.get('receiver')
            self.receiver_ad = get_object_or_404(Ad, pk=receiver_ad_id)

            sender_ads = Ad.objects.filter(user=request.user)
            self.proposal = ExchangeProposal.objects.filter(ad_receiver=self.receiver_ad, ad_sender__in=sender_ads).first()

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})

        if self.proposal:
            kwargs['instance'] = self.proposal
        else:
            kwargs['initial'] = {'ad_receiver': self.receiver_ad}

        return kwargs

    def form_valid(self, form):
        proposal = form.save()
        return JsonResponse({'status': 'ok', 'proposal_id': proposal.id})

    def post(self, request, *args, **kwargs):
        for action, status in self.ACTIONS.items():
            if request.path.endswith(f'/{action}/'):
                return self.update_proposal_status(kwargs['pk'], status)

        return super().post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        proposal = get_object_or_404(ExchangeProposal, pk=kwargs['pk'], ad_sender__user_id=request.user.id)
        proposal.delete()
        return JsonResponse({'status': 'deleted'})

    def update_proposal_status(self, pk, status):
        proposal = get_object_or_404(ExchangeProposal, pk=pk, ad_receiver__user_id=self.request.user.id)
        proposal.status = status
        proposal.save()
        return JsonResponse({'status': status})


