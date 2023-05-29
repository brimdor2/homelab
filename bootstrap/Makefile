.POSIX:

default: namespace argocd root

namespace:
	kubectl create namespace argocd --dry-run=client --output=yaml \
		| kubectl apply -f -
	sleep 10

.PHONY: argocd
argocd:
	cd argocd && ./apply.sh

.PHONY: root
root:
	cd root && ./apply.sh
