import random
from datetime import date, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth import get_user_model

from inventory.models import Warehouse, Category, Product, Incoming, IncomingItem, Outgoing, OutgoingItem
from partners.models import Supplier, Customer, SupplierPayment, CustomerPayment

User = get_user_model()

WAREHOUSES = [
    ("Asosiy ombor", "Toshkent, Yunusobod tumani, 15-uy"),
    ("Shimoliy ombor", "Toshkent, Shayxontohur tumani, 8-uy"),
    ("Janubiy ombor", "Toshkent, Sergeli tumani, 22-uy"),
    ("Markaziy ombor", "Toshkent, Mirzo Ulug'bek tumani, 5-uy"),
    ("G'arbiy ombor", "Toshkent, Uchtepa tumani, 11-uy"),
    ("Sharqiy ombor", "Toshkent, Bektemir tumani, 3-uy"),
    ("Samarqand ombori", "Samarqand, Registon ko'chasi, 7-uy"),
    ("Buxoro ombori", "Buxoro, Navruz ko'chasi, 14-uy"),
    ("Namangan ombori", "Namangan, Mustaqillik ko'chasi, 9-uy"),
    ("Farg'ona ombori", "Farg'ona, Istiqlol ko'chasi, 6-uy"),
    ("Andijon ombori", "Andijon, Navbahor ko'chasi, 2-uy"),
    ("Qo'qon ombori", "Qo'qon, Amir Temur ko'chasi, 18-uy"),
    ("Qarshi ombori", "Qarshi, Shahrisabz ko'chasi, 4-uy"),
    ("Termiz ombori", "Termiz, Surxon ko'chasi, 12-uy"),
    ("Nukus ombori", "Nukus, Berdaq ko'chasi, 20-uy"),
    ("Urganch ombori", "Urganch, Al-Xorazmiy ko'chasi, 16-uy"),
    ("Jizzax ombori", "Jizzax, Sharq ko'chasi, 10-uy"),
    ("Guliston ombori", "Guliston, Mustaqillik ko'chasi, 1-uy"),
    ("Navoiy ombori", "Navoiy, Navoiy ko'chasi, 13-uy"),
    ("Chirchiq ombori", "Chirchiq, Sanoat ko'chasi, 17-uy"),
]

CATEGORIES = [
    ("Elektronika", ),
    ("Kiyim-kechak", ),
    ("Oziq-ovqat", ),
    ("Mebel", ),
    ("Qurilish materiallari", ),
    ("Sport jihozlari", ),
    ("Kitoblar", ),
    ("O'yinchoqlar", ),
    ("Kosmetika", ),
    ("Uy-ro'zg'or buyumlari", ),
    ("Avtomobil ehtiyot qismlari", ),
    ("Tibbiy jihozlar", ),
    ("Qishloq xo'jaligi", ),
    ("Ofis jihozlari", ),
    ("Telefon aksessuarlari", ),
    ("Maishiy texnika", ),
    ("Santexnika", ),
    ("Elektr jihozlari", ),
    ("Parfyumeriya", ),
    ("Idish-tovoq", ),
]

PRODUCTS = [
    ("Samsung televizor 55\"", "dona", "8801643"),
    ("LG muzlatgich", "dona", "8806098"),
    ("Ariel kir yuvish kukuni 5kg", "kg", "5900627"),
    ("Divan uch o'rinli", "dona", ""),
    ("Sement M400 50kg", "qop", "4600123"),
    ("Futbol to'pi", "dona", "4902430"),
    ("Python dasturlash kitobi", "dona", "9781491"),
    ("Lego konstruktor 500 qism", "dona", "5702016"),
    ("L'Oreal shampun 400ml", "dona", "3600523"),
    ("Teflon qozon to'plami", "to'plam", "6923117"),
    ("Tormoz disklari Toyota", "juft", "4987456"),
    ("Qon bosimi o'lchagich", "dona", "4902777"),
    ("O'g'it azot 50kg", "qop", "4600321"),
    ("Printer HP LaserJet", "dona", "8888888"),
    ("iPhone 15 chexol", "dona", "1234567"),
    ("Kir yuvish mashinasi Ariston", "dona", "8001094"),
    ("Dush kabinasi", "dona", "4007386"),
    ("LED chiroq 12W", "dona", "4015116"),
    ("Chanel №5 atir 50ml", "dona", "3386460"),
    ("Chinni likob 6 ta", "to'plam", "4891028"),
    ("Xiaomi smartfon", "dona", "6934177"),
    ("Philips elektr ustak", "dona", "4015600"),
    ("Nike sport poyabzal", "juft", "0194501"),
    ("Krovat 160x200", "dona", ""),
    ("Gips qorishmasi 25kg", "qop", "4600456"),
    ("Tennis raketa", "dona", "4006160"),
    ("Django for Beginners kitobi", "dona", "9781735"),
    ("Barbie qo'g'irchoq", "dona", "0194735"),
    ("Nivea krem 200ml", "dona", "4005808"),
    ("Non pishirish idishi", "dona", "4006691"),
]

SUPPLIERS = [
    ("Hamkor Savdo LLC", "+998901112233", "hamkorsavdo@gmail.com", "Toshkent, Chilonzor"),
    ("Al-Baraka Import", "+998902223344", "albaraka@mail.ru", "Toshkent, Mirzo Ulug'bek"),
    ("Global Trade UZ", "+998903334455", "globaltrade@gmail.com", "Samarqand, Markaz"),
    ("Shark Optom", "+998904445566", "sharkoptom@mail.ru", "Toshkent, Yunusobod"),
    ("Silk Road Trading", "+998905556677", "silkroad@gmail.com", "Buxoro, Shahri"),
    ("Mega Distribyutor", "+998906667788", "mega@mail.ru", "Namangan, Markaz"),
    ("Dunyo Savdo", "+998907778899", "dunyosavdo@gmail.com", "Farg'ona, Markaz"),
    ("Premium Import", "+998908889900", "premium@mail.ru", "Toshkent, Shayxontohur"),
    ("Orient Express", "+998909990011", "orient@gmail.com", "Andijon, Markaz"),
    ("Baraka Optom", "+998910001122", "baraka@mail.ru", "Qarshi, Markaz"),
    ("Yangi Dunyo", "+998911112233", "yangi@gmail.com", "Termiz, Markaz"),
    ("Fayz Savdo", "+998912223344", "fayz@mail.ru", "Jizzax, Markaz"),
    ("Nur Optom", "+998913334455", "nur@gmail.com", "Navoiy, Markaz"),
    ("Zafar Trading", "+998914445566", "zafar@mail.ru", "Guliston, Markaz"),
    ("Star Import", "+998915556677", "star@gmail.com", "Urganch, Markaz"),
    ("Best Quality", "+998916667788", "bestquality@mail.ru", "Nukus, Markaz"),
    ("Top Market", "+998917778899", "topmarket@gmail.com", "Chirchiq, Markaz"),
    ("Grand Optom", "+998918889900", "grand@mail.ru", "Toshkent, Sergeli"),
    ("Victory Trade", "+998919990011", "victory@gmail.com", "Toshkent, Uchtepa"),
    ("Mustaqil Savdo", "+998920001122", "mustaqil@mail.ru", "Toshkent, Bektemir"),
]

CUSTOMERS = [
    ("Alisher Karimov", "+998901234567", "alisher@gmail.com", "Toshkent, Chilonzor"),
    ("Nodira Rahimova", "+998902345678", "nodira@mail.ru", "Toshkent, Yunusobod"),
    ("Bobur Yusupov", "+998903456789", "bobur@gmail.com", "Samarqand"),
    ("Malika Hasanova", "+998904567890", "malika@mail.ru", "Buxoro"),
    ("Jasur Toshmatov", "+998905678901", "jasur@gmail.com", "Namangan"),
    ("Dilnoza Ergasheva", "+998906789012", "dilnoza@mail.ru", "Farg'ona"),
    ("Sardor Nazarov", "+998907890123", "sardor@gmail.com", "Andijon"),
    ("Zulfiya Mirzaeva", "+998908901234", "zulfiya@mail.ru", "Qarshi"),
    ("Otabek Sobirov", "+998909012345", "otabek@gmail.com", "Termiz"),
    ("Nilufar Abdullayeva", "+998910123456", "nilufar@mail.ru", "Jizzax"),
    ("Ulugbek Xolmatov", "+998911234567", "ulugbek@gmail.com", "Navoiy"),
    ("Kamola Qodirov", "+998912345678", "kamola@mail.ru", "Guliston"),
    ("Sherzod Razzaqov", "+998913456789", "sherzod@gmail.com", "Urganch"),
    ("Mohira Yo'ldosheva", "+998914567890", "mohira@mail.ru", "Nukus"),
    ("Doniyor Xasanov", "+998915678901", "doniyor@gmail.com", "Chirchiq"),
    ("Barno Tursunova", "+998916789012", "barno@mail.ru", "Toshkent, Mirzo Ulug'bek"),
    ("Asilbek Mahmudov", "+998917890123", "asilbek@gmail.com", "Toshkent, Shayxontohur"),
    ("Gavhar Usmonova", "+998918901234", "gavhar@mail.ru", "Toshkent, Sergeli"),
    ("Mansur Qosimov", "+998919012345", "mansur@gmail.com", "Toshkent, Uchtepa"),
    ("Feruza Rajabova", "+998920123456", "feruza@mail.ru", "Toshkent, Bektemir"),
]


class Command(BaseCommand):
    help = "Barcha modellarga 20 tadan test ma'lumot qo'shadi"

    def handle(self, *args, **kwargs):
        self.stdout.write("Ma'lumotlar qo'shilmoqda...")

        with transaction.atomic():
            user = self._get_or_create_user()
            warehouses = self._seed_warehouses(user)
            categories = self._seed_categories(user)
            products = self._seed_products(user, warehouses, categories)
            suppliers = self._seed_suppliers(user)
            customers = self._seed_customers(user)
            incomings = self._seed_incomings(user, warehouses, suppliers, products)
            self._seed_outgoings(user, warehouses, customers, products)
            self._seed_supplier_payments(user, suppliers)
            self._seed_customer_payments(user, customers)

        self.stdout.write(self.style.SUCCESS("Barcha ma'lumotlar muvaffaqiyatli qo'shildi!"))

    def _get_or_create_user(self):
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={'is_superuser': True, 'is_staff': True, 'role': 'super_admin'}
        )
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write("Admin foydalanuvchi yaratildi: admin / admin123")
        return user

    def _seed_warehouses(self, user):
        self.stdout.write("  Omborlar qo'shilmoqda...")
        warehouses = []
        for name, address in WAREHOUSES:
            w, _ = Warehouse.objects.get_or_create(
                name=name,
                defaults={'address': address, 'created_by': user}
            )
            warehouses.append(w)
        self.stdout.write(f"    {len(warehouses)} ta ombor tayyor.")
        return warehouses

    def _seed_categories(self, user):
        self.stdout.write("  Kategoriyalar qo'shilmoqda...")
        categories = []
        for (name,) in CATEGORIES:
            c, _ = Category.objects.get_or_create(
                name=name,
                defaults={'created_by': user}
            )
            categories.append(c)
        self.stdout.write(f"    {len(categories)} ta kategoriya tayyor.")
        return categories

    def _seed_products(self, user, warehouses, categories):
        self.stdout.write("  Mahsulotlar qo'shilmoqda...")
        products = []
        for i, (name, unit, barcode) in enumerate(PRODUCTS):
            warehouse = warehouses[i % len(warehouses)]
            category = categories[i % len(categories)]
            initial_qty = random.randint(50, 500)
            p, created = Product.objects.get_or_create(
                name=name,
                warehouse=warehouse,
                defaults={
                    'category': category,
                    'quantity': initial_qty,
                    'initial_quantity': initial_qty,
                    'minimum_quantity': random.randint(5, 20),
                    'unit': unit,
                    'barcode': barcode or None,
                    'created_by': user,
                }
            )
            products.append(p)
        self.stdout.write(f"    {len(products)} ta mahsulot tayyor.")
        return products

    def _seed_suppliers(self, user):
        self.stdout.write("  Ta'minotchilar qo'shilmoqda...")
        suppliers = []
        for name, phone, email, address in SUPPLIERS:
            s, _ = Supplier.objects.get_or_create(
                phone_number=phone,
                defaults={
                    'name': name,
                    'email': email,
                    'address': address,
                    'initial_debt': Decimal(random.randint(0, 5000000)),
                    'created_by': user,
                }
            )
            suppliers.append(s)
        self.stdout.write(f"    {len(suppliers)} ta ta'minotchi tayyor.")
        return suppliers

    def _seed_customers(self, user):
        self.stdout.write("  Xaridorlar qo'shilmoqda...")
        customers = []
        for name, phone, email, address in CUSTOMERS:
            c, _ = Customer.objects.get_or_create(
                phone_number=phone,
                defaults={
                    'name': name,
                    'email': email,
                    'address': address,
                    'initial_debt': Decimal(random.randint(0, 2000000)),
                    'credit_limit': Decimal(random.randint(1000000, 10000000)),
                    'discount_percent': Decimal(random.randint(0, 10)),
                    'created_by': user,
                }
            )
            customers.append(c)
        self.stdout.write(f"    {len(customers)} ta xaridor tayyor.")
        return customers

    def _seed_incomings(self, user, warehouses, suppliers, products):
        self.stdout.write("  Kirimlar qo'shilmoqda...")
        incomings = []
        today = date.today()
        for i in range(20):
            incoming_date = today - timedelta(days=random.randint(1, 90))
            warehouse = warehouses[i % len(warehouses)]
            supplier = suppliers[i % len(suppliers)]
            paid = Decimal(random.randint(500000, 3000000))
            total = paid + Decimal(random.randint(0, 1000000))

            incoming = Incoming.objects.create(
                warehouse=warehouse,
                supplier=supplier,
                date=incoming_date,
                invoice_number=f"INV-2025-{i+1:04d}",
                total_amount=total,
                paid_amount=paid,
                note=f"{i+1}-kirim uchun izoh",
                created_by=user,
            )

            # Har bir kirimga 2-4 ta element qo'shish
            warehouse_products = [p for p in products if p.warehouse == warehouse]
            if not warehouse_products:
                warehouse_products = products[:3]

            selected = random.sample(warehouse_products, min(random.randint(2, 4), len(warehouse_products)))
            item_total = Decimal(0)
            for product in selected:
                qty = random.randint(10, 100)
                price = Decimal(random.randint(10000, 500000))
                item = IncomingItem.objects.create(
                    incoming=incoming,
                    product=product,
                    quantity=qty,
                    price=price,
                    total=qty * price,
                )
                item_total += item.total

            incoming.total_amount = item_total
            incoming.paid_amount = min(paid, item_total)
            incoming.debt = incoming.total_amount - incoming.paid_amount
            incoming.save()
            incomings.append(incoming)

        self.stdout.write(f"    {len(incomings)} ta kirim tayyor.")
        return incomings

    def _seed_outgoings(self, user, warehouses, customers, products):
        self.stdout.write("  Chiqimlar qo'shilmoqda...")
        today = date.today()
        count = 0
        for i in range(20):
            outgoing_date = today - timedelta(days=random.randint(1, 60))
            warehouse = warehouses[i % len(warehouses)]
            customer = customers[i % len(customers)]

            outgoing = Outgoing.objects.create(
                warehouse=warehouse,
                customer=customer,
                date=outgoing_date,
                invoice_number=f"OUT-2025-{i+1:04d}",
                total_amount=Decimal(0),
                paid_amount=Decimal(0),
                note=f"{i+1}-chiqim uchun izoh",
                created_by=user,
            )

            warehouse_products = [p for p in products if p.warehouse == warehouse and p.quantity >= 5]
            if not warehouse_products:
                outgoing.delete()
                continue

            selected = random.sample(warehouse_products, min(random.randint(1, 3), len(warehouse_products)))
            item_total = Decimal(0)
            item_profit = Decimal(0)

            for product in selected:
                available = min(product.quantity, 20)
                if available < 1:
                    continue
                qty = random.randint(1, available)
                price = Decimal(random.randint(15000, 600000))
                cost = price * Decimal('0.8')
                total = qty * price
                profit = (price - cost) * qty

                OutgoingItem.objects.create(
                    outgoing=outgoing,
                    product=product,
                    quantity=qty,
                    price=price,
                    cost_price=cost,
                    total=total,
                    profit=profit,
                )
                product.quantity -= qty
                product.save()

                item_total += total
                item_profit += profit

            paid = item_total * Decimal(str(random.uniform(0.5, 1.0))).quantize(Decimal('0.01'))
            outgoing.total_amount = item_total
            outgoing.paid_amount = paid
            outgoing.debt = item_total - paid
            outgoing.profit = item_profit
            outgoing.save()
            count += 1

        self.stdout.write(f"    {count} ta chiqim tayyor.")

    def _seed_supplier_payments(self, user, suppliers):
        self.stdout.write("  Ta'minotchi to'lovlari qo'shilmoqda...")
        today = date.today()
        payment_types = ['cash', 'card', 'transfer', 'check']
        for i in range(20):
            supplier = suppliers[i % len(suppliers)]
            SupplierPayment.objects.create(
                supplier=supplier,
                date=today - timedelta(days=random.randint(1, 60)),
                amount=Decimal(random.randint(200000, 2000000)),
                payment_type=payment_types[i % 4],
                reference_number=f"SP-{i+1:04d}",
                note=f"Ta'minotchi to'lovi #{i+1}",
                created_by=user,
            )
        self.stdout.write("    20 ta ta'minotchi to'lovi tayyor.")

    def _seed_customer_payments(self, user, customers):
        self.stdout.write("  Xaridor to'lovlari qo'shilmoqda...")
        today = date.today()
        payment_types = ['cash', 'card', 'transfer', 'check']
        for i in range(20):
            customer = customers[i % len(customers)]
            CustomerPayment.objects.create(
                customer=customer,
                date=today - timedelta(days=random.randint(1, 45)),
                amount=Decimal(random.randint(100000, 1500000)),
                payment_type=payment_types[i % 4],
                reference_number=f"CP-{i+1:04d}",
                note=f"Xaridor to'lovi #{i+1}",
                created_by=user,
            )
        self.stdout.write("    20 ta xaridor to'lovi tayyor.")
