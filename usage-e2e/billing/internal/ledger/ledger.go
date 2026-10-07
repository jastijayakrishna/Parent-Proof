package ledger

import (
	"context"
	"encoding/json"

	pb "example.com/billing/gen/paymentsv1"
)

type Ledger struct {
	client pb.PaymentsClient
}

func New(c pb.PaymentsClient) *Ledger { return &Ledger{client: c} }

func (l *Ledger) Total(ctx context.Context, id string) (int64, error) {
	charge, err := l.client.GetCharge(ctx, &pb.GetChargeRequest{Id: id})
	if err != nil {
		return 0, err
	}
	return charge.AmountCents, nil
}

func Describe(c *pb.Charge) string {
	switch c.GetStatus() {
	case pb.PaymentStatus_PAID:
		return "paid"
	case pb.PaymentStatus_REFUNDED:
		return "refunded"
	}
	return "unknown"
}

func Method(c *pb.Charge) string {
	switch m := c.GetMethod().(type) {
	case *pb.Charge_Card:
		return "card:" + m.Card
	case *pb.Charge_Bank:
		return "bank:" + m.Bank
	default:
		return "none"
	}
}

func Export(c *pb.Charge) ([]byte, error) {
	return json.Marshal(c)
}
